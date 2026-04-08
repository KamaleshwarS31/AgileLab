# Kubernetes Deployment Guide

This directory contains the Kubernetes configuration for the Weather Forecasting System.

## Prerequisites

1.  A running Kubernetes cluster (Minikube, Kind, or a cloud provider).
2.  `kubectl` CLI installed and configured.
3.  Docker images built and available in your cluster or registry:
    -   `weather-backend:latest`
    -   `weather-frontend:latest`

## Build Images (Optional)

If you haven't built the images yet, run these commands from the project root:

```bash
docker build -t weather-backend:latest ./backend
docker build -t weather-frontend:latest ./frontend
```

*Note: If using Minikube, run `eval $(minikube docker-env)` before building to make them available to the cluster.*

## Deployment Steps

1.  **Apply the configuration**:
    ```bash
    kubectl apply -f deployment.yaml
    ```

2.  **Verify the deployment**:
    ```bash
    kubectl get all -n weather-app
    ```

3.  **Access the application**:
    -   **Frontend**: Accessible via NodePort at `http://<node-ip>:30080`
    -   **Backend Docs**: Accessible via `http://<node-ip>:30080/api/docs` (if proxied) or directly via the backend service if exposed.

## Configuration

-   **API Key**: Update the `weather-secrets` in `deployment.yaml` with your base64-encoded OpenWeather API key.
-   **Service URLs**: The backend and database connections are automatically handled using Kubernetes internal DNS (e.g., `postgres-service`).

## Cleanup

To remove all resources:
```bash
kubectl delete -f deployment.yaml
```
