from datetime import datetime
from kubernetes import client, config
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

origins = [
    "http://160.85.255.146:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



kube_config_path = '/home/ubuntu/.kube/config'
# Load Kubernetes configuration (ensure kubeconfig is in the default location or provide path)
config.load_kube_config()

# Initialize the Kubernetes API client
# client1 is the client of cluster1
# client2 is the client of cluster2
client1 = client.CoreV1Api(
        api_client=config.new_client_from_config(context='cluster1'))
client2 = client.CoreV1Api(
    api_client=config.new_client_from_config(context='cluster2'))

ruleToTriggerMigration = [
    'Read sensitive file untrusted',
    'Drop and execute new binary in container',
    'Redirect STDOUT/STDIN to Network Connection in Container'
]
triggeredMigrations = []
activeClient = client1

@app.post("/trigger-migration/")
async def handle_warning(request: Request):
    body = await request.json()
    hostname = body.get("hostname")
    rule = body.get("rule")
    priority = body.get("priority")
    k8s_pod_name = body.get("output_fields", {}).get("k8s.pod.name")
    container_name = body.get("output_fields", {}).get("container.name")

    if rule in ruleToTriggerMigration and k8s_pod_name not in triggeredMigrations:
        triggeredMigrations.append(k8s_pod_name)
        print(f"Security event with priority {priority} and rule {rule} received from {hostname}")
        print(f"Migrating pod {k8s_pod_name} to a secure cluster")
        os.makedirs(f"/home/ubuntu/contMigration_logs/{container_name}/{k8s_pod_name}", exist_ok=True)
        with open(f"/home/ubuntu/contMigration_logs/{container_name}/{k8s_pod_name}/forensic_report.txt", "w") as file:
            file.write(f"Forensic report of automated container migration of {k8s_pod_name}\n")
            file.write(f"Migration is triggered because of falco rule of:\n{rule}\nreceived on {hostname}\n")
            file.write(f"Migration is triggered at {datetime.now()}\n\n")
        return await trigger_migration(k8s_pod_name)


async def trigger_migration(k8s_pod_name):
    try:
        # Run the migration script located at /host/migration.sh
        result = subprocess.run(["../../scripts/migration/single-migration.sh", k8s_pod_name], check=True, capture_output=True, text=True, timeout=120)

        # Return the result of the script execution
        return {"message": "Migration script executed successfully", "output": result.stdout}

    except subprocess.CalledProcessError as e:
    # Handle errors if the script fails
        raise HTTPException(status_code=500, detail=f"Error executing script: {e.stderr}")


# Add an endpoint to get the list of pods in the cluster (for debugging or other purposes)
@app.get("/k8s/pods/{cluster}")
async def get_pods(cluster: str):
    """Get a list of pods in the specified Kubernetes namespace"""
    set_active_cluster(cluster)
    try:
        pods = activeClient.list_namespaced_pod(namespace='default')
        
        pod_info = [
            {"name": pod.metadata.name, "status": pod.status.phase}
            for pod in pods.items
        ]
        
        return {"pods": pod_info}
    
    except client.exceptions.ApiException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pods: {e}")

@app.delete("/k8s/pods/{cluster}/{pod_name}")
async def delete_pod(cluster: str, pod_name: str):
    """Delete a Kubernetes pod by its name."""
    set_active_cluster(cluster)
    try:
        # Delete the pod
        response = activeClient.delete_namespaced_pod(
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
            detail=f"Failed to delete pod '{pod_name}' in namespace '{namespace}': {e.reason}",
        )


def set_active_cluster(targetCluster: str):
    global activeClient
    if targetCluster == 'cluster1':
        activeClient = client1
    elif targetCluster == 'cluster2':
        activeClient = client2
    else: 
        raise ValueError(f"Invalid client choice: {client_choice}")

    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("migration:app", host="0.0.0.0", port=8000, reload=True)
