# Project X – DevOps Dashboard

## Overview

DevOps Dashboard is a Raspberry Pi-based dashboard application designed to display useful system, application and DevOps-related information in a local UI.

The project combines a native PyQt frontend running directly on the Raspberry Pi display with a containerized backend and database managed through Kubernetes. The full deployment process is automated with Jenkins, Docker and GitHub.

This project demonstrates how to:

- build a complete CI/CD workflow for an edge device;
- deploy a native PyQt UI directly on a Raspberry Pi;
- containerize and deploy backend services with Docker and Kubernetes;
- manage application restarts using systemd;
- separate frontend, backend and database responsibilities.

## Architecture

```text
Developer Laptop
    |
    | git push
    v
GitHub Repository
    |
    v
Jenkins Pipeline
    |
    |-----------------------------|
    |                             |
    v                             v
Build & Push Backend Image     Copy PyQt UI to Raspberry Pi
    |                             |
    v                             v
Docker Registry              Restart UI with systemd
    |
    v
Raspberry Pi - k3s/Kubernetes
    |
    |-- Backend API container
    |-- Database container
    |
    v
PyQt UI -> Backend API -> Database
```