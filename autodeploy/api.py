from fastapi import FastAPI
from pydantic import BaseModel
from autodeploy.engine import deploy

class DeployReq(BaseModel):
    instruction: str
    repo: str | None = None
    zip_path: str | None = None
    region: str = "us-west-2"

app = FastAPI()

@app.post("/deploy")
def deploy_ep(req: DeployReq):
    out = deploy(
        instruction=req.instruction,
        repo=req.repo,
        zip_path=req.zip_path,
        cloud={"name": "aws", "region": req.region},
        compute={"instance_type": "t3.micro", "key_name": None},
        net={"open_ports": [80]},
    )
    return out
