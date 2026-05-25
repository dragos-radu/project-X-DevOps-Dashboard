# Kubernetes Manifests

This folder contains the initial Kubernetes manifests for the DevOps Dashboard backend and database.

## Components

- Namespace for the application
- PostgreSQL database deployment
- Persistent volume claim for database data
- Internal database service
- Backend deployment
- Backend NodePort service

## Communication

The backend connects to PostgreSQL using the Kubernetes service name:

```text
database
```

## Manual Deployment

Apply the manifests manually on the Raspberry Pi k3s cluster:

```bash
kubectl apply -f k8s/
```

Check the resources:

```bash
kubectl get all -n devops-dashboard
```

Test backend:

```bash
curl http://<raspberry-pi-ip>:30001/api/health
```