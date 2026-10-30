# pulse

Pulse is a small uptime monitor: you give it a list of websites and it regularly checks each one and reports whether it's up, what HTTP status code it returned, and how long it took to respond.

## Repository structure

- `app/`: the Pulse application, Python code and its Dockerfile.
- `ansible/`: Ansible playbooks that set up the Linux server automatically (users, SSH, firewall, k3s).
- `k8s/`: Kubernetes manifests that describe the desired state of the app in the cluster.
- `helm/`: the Pulse app packaged as a Helm chart, deployed by ArgoCD.
- `scripts/`: Bash scripts for everyday operational tasks.
- `.github/workflows/`: CI pipeline definitions that run on every push and pull request.
