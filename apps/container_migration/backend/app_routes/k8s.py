from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from utils.k8s_client import k8s_client 

router = APIRouter()

@router.get("/pods/{cluster}")
async def get_pods(cluster: str):
    """Get a list of pods in the specified Kubernetes namespace"""
    client = k8s_client.get_client(cluster)
    try:
        pods = client.list_namespaced_pod(namespace='default')
        podsList = []
        for pod in pods.items:
            pod_info = dict({
                "podName": pod.metadata.name, 
                "appName": pod.metadata.labels.get('app', 'N/A'), 
                "status": pod.status.phase,
                "age": format_age(datetime.now(timezone.utc) - pod.metadata.creation_timestamp)
            })

            if pod.status.phase == "Pending" and pod.status.container_statuses:
                waiting_reason = pod.status.container_statuses[0].state.waiting.reason if pod.status.container_statuses[0].state.waiting else "Unknown"
                pod_info.update({"reason": waiting_reason})
            
            podsList.append(pod_info)
        
        return {"pods": podsList}
    
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


def format_age(age: timedelta) -> str:
    days = age.days
    seconds = age.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        if hours > 0:
            return f"{days}d{hours}h"
        else:
            return f"{days}d"
    elif hours > 0:
        return f"{hours}h{minutes}m"
    else:
        return f"{minutes}m"
