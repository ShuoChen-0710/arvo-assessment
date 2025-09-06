import tempfile, zipfile
from pathlib import Path
from git import Repo


def fetch_repo(repo: str | None, zip_path: str | None, workdir: Path) -> Path:
    app_dir = workdir / "app"
    if repo:
        Repo.clone_from(repo, app_dir)
        return app_dir
    if zip_path:
        app_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(app_dir)
        return app_dir
    raise ValueError("Either --repo or --zip_path must be provided")
