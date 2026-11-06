# Pulse

Pulse is a small uptime monitor: give it a list of websites and it checks each one on request, reporting whether it's up, what HTTP status code it returned, and how long it took to respond.

Built as a hands-on DevOps portfolio project, covering the full path from a Python app to a self-healing, GitOps-managed Kubernetes deployment: Git workflow, Docker, CI, Ansible server provisioning, Kubernetes, Helm, and ArgoCD.

## Architecture

```
Browser/curl
│
▼
Traefik Ingress (pulse.local)
│
▼
Kubernetes Service (pulse, ClusterIP)
│
▼
Kubernetes Deployment → Pod(s) running the Flask app (gunicorn)
```

Everything in the cluster — the Deployment, Service, and Ingress — is defined as a Helm chart (`helm/pulse/`) and deployed by **ArgoCD**, which continuously syncs the cluster to match what's committed on `master`. Deploying means merging a pull request; nothing is ever applied to the cluster by hand.

## Repository structure

- `app/` — the Pulse Flask application and its Dockerfile.
- `ansible/` — playbooks that provision the server: firewall (ufw), SSH hardening, and k3s installation.
- `helm/pulse/` — the Pulse app packaged as a Helm chart (Deployment, Service, Ingress), the single source of truth for what's deployed.
- `argocd/` — the ArgoCD `Application` definition that tells ArgoCD to watch this repo and sync `helm/pulse/` into the cluster.
- `scripts/` — Bash scripts for everyday operational tasks (e.g. `status.sh`, a quick health check).
- `.github/workflows/` — CI pipeline: builds the Docker image on every pull request.

## Endpoints

- `GET /health` — liveness check, returns `{"status": "ok"}`.
- `GET /status` — checks every site listed in the `PULSE_SITES` environment variable, returns up/down, HTTP status code, and response time for each.

## Running it

**Locally, without Kubernetes:**

```bash
cd app
pip install -r requirements.txt
PULSE_SITES="https://github.com,https://www.google.com" python3 main.py
```

**As a container:**

```bash
docker build -t pulse:local app
docker run -p 5000:5000 -e PULSE_SITES="https://github.com" pulse:local
```

**On Kubernetes, via Helm (manually, outside the GitOps flow):**

```bash
helm install pulse helm/pulse
```

In this project's actual setup, deployment happens automatically: ArgoCD watches this repo and applies `helm/pulse/` to the cluster on every push to `master`.

## Infrastructure

The app runs on a single Ubuntu Server VM running [k3s](https://k3s.io/) (lightweight Kubernetes), provisioned entirely through Ansible: firewall rules, SSH key-only hardening, and the k3s install itself are all idempotent playbook tasks, not manual steps.

## Screenshots

(see `docs/images/`)

## What this project demonstrates

- Git: branching, conventional commits, PRs, squash merges
- Docker: multi-stage-aware layering, non-root containers, production WSGI server (gunicorn)
- CI: GitHub Actions building the image on every PR
- Linux/networking: SSH, firewalls, DNS, troubleshooting real connectivity issues
- Ansible: idempotent, repeatable server configuration
- Kubernetes: Deployments, Services, Ingress, debugging real Pod failures
- Helm: templated manifests with environment-specific values
- ArgoCD/GitOps: Git as the single source of truth, self-healing deployments
