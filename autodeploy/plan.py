from dataclasses import dataclass

@dataclass
class DeploymentPlan:
    cloud: dict
    compute: dict
    net: dict
    app_dir: str
    run_dir: str
    start_cmd: str
    use_docker: bool

    @staticmethod
    def from_detect(instruction: str, detect: dict, cloud: dict, compute: dict, net: dict, app_dir: str, run_dir: str):
        use_docker = bool(detect.get("has_docker"))
        start_cmd = detect.get("start_cmd") or "echo 'No start command detected'"
        return DeploymentPlan(
            cloud=cloud, compute=compute, net=net,
            app_dir=app_dir, run_dir=run_dir,
            start_cmd=start_cmd, use_docker=use_docker,
        )
