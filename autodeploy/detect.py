import json
from pathlib import Path

PY_HINTS = ["requirements.txt", "pyproject.toml"]
NODE_HINTS = ["package.json"]


def detect_stack(app_dir: Path) -> dict:
    p = Path(app_dir)
    has_docker = (p / "Dockerfile").exists()

    kind = None
    port = 80
    cmd = None

    if (p / "package.json").exists():
        kind = "node"
        # naive: if express present, assume `node server.js` or `npm start`
        cmd = "npm install && npm run start || node server.js || node app.js"

    if any((p / x).exists() for x in PY_HINTS):
        # look for common python web servers
        kind = "python"
        # try to guess entry
        entry = guess_python_entry(p)
        cmd = f"pip install -r requirements.txt || true; pip install gunicorn uvicorn || true; gunicorn -b 0.0.0.0:80 {entry} || uvicorn {entry}:app --host 0.0.0.0 --port 80"

    if (p / "manage.py").exists():
        kind = "django"
        cmd = "pip install -r requirements.txt || true; python manage.py migrate --noinput; gunicorn -b 0.0.0.0:80 config.wsgi:application || gunicorn -b 0.0.0.0:80 <project>.wsgi:application"

    if has_docker:
        kind = (kind or "generic") + "+docker"

    return {"kind": kind or "generic", "has_docker": has_docker, "port": port, "start_cmd": cmd}


def guess_python_entry(p: Path) -> str:
    # try common names for Flask/FastAPI
    for name in ["app", "main", "server", "wsgi", "application"]:
        if (p / f"{name}.py").exists():
            return f"{name}:app"
    # otherwise fallback to package.module:app if a single package exists
    pkgs = [d.name for d in p.iterdir() if d.is_dir() and (p / d / "__init__.py").exists()]
    if pkgs:
        return f"{pkgs[0]}.app"
    return "app:app"
