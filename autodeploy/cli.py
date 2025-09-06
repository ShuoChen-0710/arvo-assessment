import json, uuid, typer
from pathlib import Path
from autodeploy.engine import deploy

app = typer.Typer(add_completion=False)

@app.command()
def main(
    instruction: str = typer.Argument(..., help="Natural language deployment intent"),
    repo: str = typer.Option(None, help="Git URL or local path"),
    zip_path: str = typer.Option(None, help="Path to a ZIP file containing the app"),
    region: str = typer.Option("us-west-2", help="AWS region"),
    instance_type: str = typer.Option("t3.micro", help="EC2 instance type"),
    key_name: str = typer.Option(None, help="Optional EC2 key pair name for SSH"),
    open_ports: str = typer.Option("80", help="Comma-separated ports to open"),
):
    run_id = str(uuid.uuid4())[:8]
    result = deploy(
        instruction=instruction,
        repo=repo,
        zip_path=zip_path,
        cloud={"name": "aws", "region": region},
        compute={"instance_type": instance_type, "key_name": key_name},
        net={"open_ports": [int(p) for p in open_ports.split(',') if p]},
        run_id=run_id,
    )
    typer.secho(json.dumps(result, indent=2), fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
