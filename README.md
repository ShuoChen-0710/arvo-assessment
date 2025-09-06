### Title
**Arvo AutoDeploy** – Natural‑Language to Cloud in One Command

### Demo
- 60‑second Loom walkthrough (script below).

### How it works
1. Parse your instruction, clone/unzip the repo.
2. Detect the stack and choose a deploy strategy (Docker → Python → Node).
3. Render Terraform + cloud‑init via Jinja2; apply with Terraform.
4. Return the VM public IP and write logs.

### Usage
- **CLI:** see Quickstart.
- **API:** `POST /deploy` as shown above.

### Configuration
- `AWS_REGION` via flag; instance type via `--instance-type`.
- Open ports via `--open-ports` (default: 80).
- Use your own key pair via `--key-name`.

### Uninstall / Destroy
```bash
cd .autodeploy/<run-id>/terraform && terraform destroy -auto-approve
```

### Limitations
- Works best for simple Flask/FastAPI/Express or Dockerized apps.
- For complex Django/mono‑repos, provide a Dockerfile for reliability.
- Assumes public internet egress and default VPC.

### Roadmap
- Add GCP/Azure modules
- Secrets manager + env injection
- Managed DB/Redis modules
- Health checks and retry strategies

### License
MIT

### Credits & Sources (to put in README)
- HashiCorp Terraform & AWS Provider docs
- FastAPI & Typer docs
- GitPython docs
- Ubuntu cloud‑init docs

```
