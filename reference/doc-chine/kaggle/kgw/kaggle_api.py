"""Petit client REST pour l'API publique Kaggle (https://www.kaggle.com/api/v1).

Un seul compte. Authentification, dans cet ordre :
  1. KGW_KAGGLE_AUTH=none            -> aucun en-tête (proxy qui ajoute lui-même l'authentification)
  2. KAGGLE_USERNAME + KAGGLE_KEY    -> Basic (token "legacy" de kaggle.json)
  3. KAGGLE_API_TOKEN                -> Bearer (nouveaux tokens Kaggle)
  4. ~/.kaggle/kaggle.json (ou $KAGGLE_CONFIG_DIR/kaggle.json) -> Basic
  5. ~/.kaggle/access_token          -> Bearer
"""
from __future__ import annotations

import base64
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

import httpx

log = logging.getLogger("kgw.kaggle")
API = "https://www.kaggle.com/api/v1"


class KaggleError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, retryable: bool = False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


# Messages Kaggle qui signifient "réessayez plus tard" (sessions simultanées, file d'attente...)
_RETRY_HINTS = ("concurrent", "session", "too many", "rate limit", "try again", "temporarily", "busy", "maximum")
_QUOTA_HINTS = ("quota",)


def _config_dir() -> Path:
    return Path(os.environ.get("KAGGLE_CONFIG_DIR") or Path.home() / ".kaggle")


def resolve_auth() -> tuple[dict[str, str], str, str]:
    """-> (en-têtes, nom d'utilisateur, description de la méthode)"""
    user = os.environ.get("KAGGLE_USERNAME", "") or os.environ.get("KGW_KAGGLE_USERNAME", "")
    if os.environ.get("KGW_KAGGLE_AUTH", "").lower() == "none":
        return {}, user, "aucune (proxy)"
    key = os.environ.get("KAGGLE_KEY", "")
    if user and key:
        tok = base64.b64encode(f"{user}:{key}".encode()).decode()
        return {"Authorization": f"Basic {tok}"}, user, "KAGGLE_USERNAME/KAGGLE_KEY"
    tok = os.environ.get("KAGGLE_API_TOKEN", "")
    if tok:
        return {"Authorization": f"Bearer {tok}"}, user, "KAGGLE_API_TOKEN"
    kj = _config_dir() / "kaggle.json"
    if kj.is_file():
        d = json.loads(kj.read_text())
        user = user or d.get("username", "")
        if d.get("key"):
            tok = base64.b64encode(f"{d['username']}:{d['key']}".encode()).decode()
            return {"Authorization": f"Basic {tok}"}, user, str(kj)
    at = _config_dir() / "access_token"
    if at.is_file():
        return {"Authorization": f"Bearer {at.read_text().strip()}"}, user, str(at)
    raise KaggleError("Aucun token Kaggle trouvé : définissez KAGGLE_USERNAME et KAGGLE_KEY, "
                      "ou placez kaggle.json dans ~/.kaggle/ (voir README).")


class KaggleAPI:
    def __init__(self, username: str = ""):
        headers, user, self.auth_method = resolve_auth()
        self.username = username or user
        if not self.username:
            raise KaggleError("Nom d'utilisateur Kaggle inconnu : définissez KAGGLE_USERNAME.")
        self.http = httpx.Client(base_url=API, headers={**headers, "User-Agent": "kaggle-gateway/1.0"},
                                 timeout=httpx.Timeout(120, connect=30), follow_redirects=True)
        # client séparé, sans en-tête d'authentification, pour les URL signées (stockage Google)
        self.raw = httpx.Client(timeout=httpx.Timeout(600, connect=30), follow_redirects=True)

    # ------------------------------------------------------------------ bas niveau
    def _req(self, method: str, path: str, **kw) -> Any:
        last = None
        for attempt in range(4):
            try:
                r = self.http.request(method, path, **kw)
            except httpx.HTTPError as e:   # réseau : on réessaie
                last = e
                time.sleep(3 * (attempt + 1))
                continue
            if r.status_code in (429, 500, 502, 503, 504):
                last = KaggleError(f"Kaggle {r.status_code}: {r.text[:300]}", r.status_code, True)
                time.sleep(5 * (attempt + 1))
                continue
            if r.status_code == 401 or r.status_code == 403:
                raise KaggleError(f"Kaggle refuse l'authentification ({r.status_code}). Vérifiez votre token. {r.text[:200]}",
                                  r.status_code)
            if r.status_code >= 400:
                msg = r.text[:500]
                low = msg.lower()
                raise KaggleError(f"Kaggle {r.status_code}: {msg}", r.status_code,
                                  retryable=any(h in low for h in _RETRY_HINTS) and not any(h in low for h in _QUOTA_HINTS))
            try:
                return r.json()
            except ValueError:
                return r.text
        raise KaggleError(f"Kaggle injoignable : {last}", retryable=True)

    def whoami_check(self) -> dict:
        """Vérifie que le token fonctionne (liste ses propres notebooks)."""
        d = self._req("GET", "/kernels/list", params={"user": self.username, "pageSize": 1})
        return {"username": self.username, "auth": self.auth_method, "ok": isinstance(d, list)}

    # ------------------------------------------------------------------ datasets
    def upload_file(self, path: Path, name: str | None = None) -> str:
        """Envoie un fichier vers le stockage Kaggle, renvoie le token à joindre au dataset."""
        path = Path(path)
        size = path.stat().st_size
        d = self._req("POST", f"/datasets/upload/file/{size}/{int(path.stat().st_mtime)}",
                      data={"fileName": name or path.name})
        if not isinstance(d, dict) or not d.get("createUrl"):
            raise KaggleError(f"Réponse inattendue de Kaggle (upload) : {str(d)[:300]}")
        for attempt in range(3):
            try:
                with path.open("rb") as f:
                    r = self.raw.put(d["createUrl"], content=f, headers={"Content-Length": str(size)})
                if r.status_code < 300:
                    return d["token"]
                err = f"{r.status_code} {r.text[:200]}"
            except httpx.HTTPError as e:
                err = str(e)
            time.sleep(5 * (attempt + 1))
        raise KaggleError(f"Envoi du fichier {path.name} impossible : {err}", retryable=True)

    def dataset_status(self, slug: str) -> str:
        d = self._req("GET", f"/datasets/status/{self.username}/{slug}")
        return str(d).strip('"').lower()

    def dataset_version(self, slug: str) -> int:
        """Numéro de la version courante du dataset (0 s'il n'existe pas)."""
        try:
            d = self._req("GET", f"/datasets/view/{self.username}/{slug}")
        except KaggleError as e:
            if e.status in (400, 403, 404):
                return 0
            raise
        return int(d.get("currentVersionNumber") or 0) if isinstance(d, dict) else 0

    def put_dataset_files(self, slug: str, files: dict[str, Path], note: str) -> int:
        """Remplace le contenu du dataset privé `slug` par `files` (nouvelle version, anciennes supprimées).
        Renvoie le numéro de la nouvelle version : il faut l'épingler dans le notebook (owner/slug/versions/N),
        sinon un notebook lancé juste après peut démarrer sans les fichiers."""
        v0 = self.dataset_version(slug)
        tokens = [{"token": self.upload_file(p, name)} for name, p in files.items()]
        body = {"versionNotes": note[:200], "files": tokens, "deleteOldVersions": True,
                "convertToCsv": False, "categoryIds": []}
        try:
            d = self._req("POST", f"/datasets/create/version/{self.username}/{slug}", json=body)
            if isinstance(d, dict) and d.get("error"):
                raise KaggleError(d["error"], 404)
        except KaggleError as e:
            if e.status not in (400, 404) and "not found" not in str(e).lower():
                raise
            log.info("Dataset %s absent : création (privé)", slug)
            body = {"ownerSlug": self.username, "slug": slug, "title": f"{slug} (kaggle gateway)",
                    "licenseName": "unknown", "isPrivate": True, "convertToCsv": False, "files": tokens,
                    "subtitle": "", "description": "Fichiers d'entrée privés de la passerelle locale.", "categoryIds": []}
            d = self._req("POST", "/datasets/create/new", json=body)
            if isinstance(d, dict) and d.get("error"):
                raise KaggleError(f"Création du dataset impossible : {d['error']}")
        # attendre que Kaggle ait enregistré ET traité la nouvelle version
        t0 = time.time()
        while time.time() - t0 < 600:
            v = self.dataset_version(slug)
            st = self.dataset_status(slug) if v > v0 else "pending"
            if st == "ready":
                return v
            if st in ("error", "failed"):
                raise KaggleError(f"Kaggle n'a pas pu traiter le dataset {slug} ({st})")
            time.sleep(4)
        raise KaggleError(f"Dataset {slug} toujours en traitement après 10 min", retryable=True)

    # ------------------------------------------------------------------ notebooks (kernels)
    def push_kernel(self, slug: str, title: str, notebook: dict, *, gpu: bool = True, internet: bool = True,
                    datasets: list[str] | None = None, machine_shape: str = "NvidiaTeslaT4") -> int:
        text = json.dumps(notebook)
        if len(text.encode()) >= 1_000_000:
            raise KaggleError("Notebook trop gros (> 1 Mo) : réduisez KGW_INLINE_MAX_BYTES.")
        body = {"slug": f"{self.username}/{slug}", "newTitle": title, "text": text, "language": "python",
                "kernelType": "notebook", "isPrivate": True, "enableGpu": gpu, "enableInternet": internet,
                "enableTpu": False, "datasetDataSources": [f"{self.username}/{d}" for d in (datasets or [])],
                "competitionDataSources": [], "kernelDataSources": [], "modelDataSources": [], "categoryIds": []}
        if gpu:
            body["machineShape"] = machine_shape
        d = self._req("POST", "/kernels/push", json=body)
        if isinstance(d, dict) and d.get("error"):
            low = d["error"].lower()
            raise KaggleError(f"Kaggle refuse le notebook : {d['error']}", 400,
                              retryable=any(h in low for h in _RETRY_HINTS) and not any(h in low for h in _QUOTA_HINTS))
        if isinstance(d, dict) and (d.get("invalidDatasetSources") or []):
            raise KaggleError(f"Dataset invalide : {d['invalidDatasetSources']}")
        return int(d.get("versionNumber") or 0) if isinstance(d, dict) else 0

    def kernel_status(self, slug: str) -> tuple[str, str]:
        d = self._req("GET", "/kernels/status", params={"userName": self.username, "kernelSlug": slug})
        return (d.get("status") or "unknown").lower(), d.get("failureMessage") or ""

    def kernel_output(self, slug: str) -> tuple[str, list[dict]]:
        """-> (texte du log, [{fileName, url}]). Disponible seulement quand le notebook est terminé."""
        d = self._req("GET", "/kernels/output", params={"userName": self.username, "kernelSlug": slug})
        text = ""
        try:
            text = "".join(x.get("data", "") for x in json.loads(d.get("log") or "[]"))
        except Exception:
            text = str(d.get("log") or "")
        return text, list(d.get("files") or [])

    def download(self, url: str, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with self.raw.stream("GET", url) as r:
            if r.status_code >= 400:
                raise KaggleError(f"Téléchargement impossible ({r.status_code})", retryable=True)
            with dest.open("wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    f.write(chunk)
        return dest

    def kernel_url(self, slug: str) -> str:
        return f"https://www.kaggle.com/code/{self.username}/{slug}"
