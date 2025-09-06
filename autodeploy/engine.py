import os, json, subprocess, shutil
from pathlib import Path
from .detect import detect_stack
from .plan import DeploymentPlan
from .render import render_and_apply
from .repo_io import fetch_repo
from .logging_utils import JsonlLogger


def deploy(instruction, repo, zip_path, cloud, compute, net, run_id: str | None = None):
    work = Path(".autodeploy") / (run_id or "run")
    work.mkdir(parents=True, exist_ok=True)
    logger = JsonlLogger(work / "deploy_log.jsonl")

    logger.log(step="parse_instruction", ok=True, detail={"instruction": instruction})

    app_dir = fetch_repo(repo=repo, zip_path=zip_path, workdir=work)

    detect = detect_stack(app_dir)
    logger.log(step="detect_stack", ok=True, detail=detect)

    plan = DeploymentPlan.from_detect(
        instruction=instruction,
        detect=detect,
        cloud=cloud,
        compute=compute,
        net=net,
        app_dir=str(app_dir),
        run_dir=str(work)
    )

    tf_dir = work / "terraform"
    result = render_and_apply(plan, tf_dir, logger)

    return {
        "public_ip": result.get("public_ip"),
        "http": f"http://{result.get('public_ip')}",
        "terraform_dir": str(tf_dir.resolve()),
        "logs_path": str((work / "deploy_log.jsonl").resolve()),
        "detect": detect,
    }
