---
id: 2
title: k8s-minikube-deployment-plan
stage: plan
date_iso: 2026-01-11
surface: agent
model: Qwen
feature: k8s-minikube-deployment
branch: 16-k8s-minikube-deployment
user: Assistant
command: /sp.plan
labels: ["kubernetes", "deployment", "minikube", "todo-app", "helm", "docker"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/16-k8s-minikube-deployment/plan.md
  - specs/16-k8s-minikube-deployment/research.md
  - specs/16-k8s-minikube-deployment/data-model.md
  - specs/16-k8s-minikube-deployment/quickstart.md
  - specs/16-k8s-minikube-deployment/contracts/backend-api.yaml
tests_yaml: []
prompt_text: "/sp.plan # sp.plan — Phase IV: Local Kubernetes Deployment on Windows 10\n          Minikube + VirtualBox + Helm Charts\n          Branch: phase4-k8s-windows\n          Date: January 11, 2026\n\n## Core Constraints — Windows 10 (Home/Pro ≤ 22H2)\n- Hyper-V usually not available or disabled on Home edition\n- Latest Docker Desktop (4.30+) often refuses to install or enable Kubernetes on Windows 10\n- Gordon (Docker AI agent) → mostly unavailable / very limited on Windows 10\n- kubectl-ai & kagent → almost never work reliably on Windows 10 in 2026\n→ Conclusion: we will use **manual/classic** workflow with VirtualBox driver\n\n## Final Decision — Realistic Stack for Windows 10 in 2026\nContainer runtime  → minikube's built-in docker (via minikube docker-env)\nOrchestration     → minikube (driver=virtualbox)\nPackage manager   → Helm 3 (binary or chocolatey)\nImage building    → docker CLI inside minikube VM (no local Docker Desktop needed)\nAI assistance     → NONE (Gordon / kubectl-ai / kagent skipped or manual prompt only)\n\n## Acceptance Goals (what must work at the end)\n1. minikube cluster starts with virtualbox driver\n2. frontend & backend images built **inside** minikube\n3. basic Helm chart deploys both services\n4. frontend reachable via browser (minikube service … --url)\n5. login + task list + chatbot endpoint responds\n\n## Phase-by-phase Execution Order\n\nPhase 0 – One-time Prerequisites (do once)\n─────────────────────────────────────────────\n[ ] VirtualBox ≥ 7.0 installed[](https://www.virtualbox.org/)\n[ ] Virtualization (VT-x / AMD-V) enabled in BIOS\n[ ] Chocolatey installed[](https://chocolatey.org/install)\n[ ] minikube, kubectl, helm installed via choco\n\n    choco install minikube kubernetes-cli kubernetes-helm\n\nPhase 1 – Cluster Bootstrap (10–25 min)\n─────────────────────────────────────────────\n1. Delete old broken cluster (if any)\n\n   minikube delete --all --purge\n\n2. Start fresh cluster with virtualbox\n\n   minikube start --driver=virtualbox --cpus=2 --memory=4096 --disk-size=20000mb\n\n   Expected: \"minikube started\" + \"Done! kubectl is now configured…\"\n\n3. Verify\n\n   minikube status\n   kubectl get nodes\n\nPhase 2 – Use minikube's docker daemon (the most important Windows trick)\n───────────────────────────────────────────────────────────────────────────\nRun this **every new PowerShell session** before building images:\n\n   minikube docker-env | Invoke-Expression\n\n   # You should see output like:\n   # $Env:DOCKER_HOST        = \"tcp://192.168.99.100:2376\"\n   # $Env:DOCKER_CERT_PATH   = \"...\"\n   # ...\n\nPhase 3 – Build images inside minikube (15–40 min)\n─────────────────────────────────────────────────────\n1. Frontend image\n\n   cd frontend\n   docker build -t todo-frontend:local -f ../docker/frontend/Dockerfile .\n\n2. Backend image\n\n   cd ../backend\n   docker build -t todo-backend:local -f ../docker/backend/Dockerfile .\n\n3. Verify images exist in minikube\n\n   minikube image ls | findstr todo-\n\nPhase 4 – Create minimal Helm chart (30–60 min)\n─────────────────────────────────────────────────\nFolder structure:\n\ncharts/todo-app/\n├── Chart.yaml\n├── values.yaml\n└── templates/\n    ├── frontend-deployment.yaml\n    ├── frontend-service.yaml\n    ├── backend-deployment.yaml\n    └── backend-service.yaml\n\nMinimal content examples:\n\nChart.yaml\n```yaml\napiVersion: v2\nname: todo-app\ndescription: Todo Chatbot\nversion: 0.1.0"
response_text: "Created implementation plan for local Kubernetes deployment of the Todo Chatbot application. Generated plan.md with technical context, constitution check, and project structure. Created research.md with technology decisions, data-model.md with Kubernetes resources, quickstart.md with deployment instructions, and backend-api.yaml with OpenAPI contract. All artifacts are in specs/16-k8s-minikube-deployment/ directory."
outcome: "Successfully created comprehensive implementation plan for Kubernetes deployment of Todo Chatbot application with Minikube on Windows 10. The plan includes all necessary components: technical context, research, data models, quickstart guide, and API contracts. Ready for the task breakdown phase (/sp.tasks)."
evaluation: "Plan meets all requirements with clear technical approach, appropriate technology choices for Windows 10 constraints, and comprehensive documentation. Successfully addressed the challenge of deploying to Kubernetes on Windows 10 using VirtualBox instead of Hyper-V."
---