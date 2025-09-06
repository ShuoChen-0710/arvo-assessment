import os, subprocess, shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_and_apply(plan, tf_dir: Path, logger):
    env = Environment(loader=FileSystemLoader(str(Path(__file__).parent / "templates" / "terraform")))

    tf_dir.mkdir(parents=True, exist_ok=True)
    # write static files
    shutil.copyfile(Path(__file__).parent / "templates" / "terraform" / "outputs.tf", tf_dir / "outputs.tf")
    shutil.copyfile(Path(__file__).parent / "templates" / "terraform" / "variables.tf", tf_dir / "variables.tf")

    # render templated files
    for name in ["main.tf.j2", "user_data.sh.j2"]:
        tmpl = env.get_template(name)
        out = tmpl.render(plan=plan)
        (tf_dir / name.replace(".j2", "")).write_text(out)

    logger.log(step="terraform_init", ok=True)
    run(["terraform", "init"], cwd=tf_dir, logger=logger)

    logger.log(step="terraform_apply", ok=True)
    run(["terraform", "apply", "-auto-approve"], cwd=tf_dir, logger=logger)

    ip = run(["terraform", "output", "-raw", "public_ip"], cwd=tf_dir, logger=logger).strip()
    return {"public_ip": ip}


def run(cmd, cwd, logger):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    logger.log(step="exec", ok=p.returncode==0, detail={"cmd": cmd, "stdout": p.stdout, "stderr": p.stderr})
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout
