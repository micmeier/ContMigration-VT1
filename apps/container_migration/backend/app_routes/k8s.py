from fastapi import APIRouter, HTTPException
from utils.k8s_client import k8s_client 

router = APIRouter()

@router.get("/pods/{cluster}")
async def get_pods(cluster: str):
    """Get a list of pods in the specified Kubernetes namespace"""
    client = k8s_client.get_client(cluster)
    try:
        pods = client.list_namespaced_pod(namespace='default')
        
        pod_info = [
            {"name": pod.metadata.name, "status": pod.status.phase}
            for pod in pods.items
        ]
        
        return {"pods": pod_info}
    
    except client.exceptions.ApiException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pods: {e}")

@router.delete("/pods/{cluster}/{pod_name}")
async def delete_pod(cluster: str, pod_name: str):
    """Delete a Kubernetes pod by its name."""
    client = k8s_client.get_client(cluster)
    try:
        response = client.delete_namespaced_pod(
            name=pod_name,
            namespace='default'
        )
        return {
            "message": f"Pod '{pod_name}' deleted successfully in cluster '{cluster}'"
        }
    except client.exceptions.ApiException as e:
        # Handle Kubernetes API exceptions
        raise HTTPException(
            status_code=e.status,
            detail=f"Failed to delete pod '{pod_name}' in cluster '{cluster}': {e.reason}",
        )
