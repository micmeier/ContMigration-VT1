from datetime import datetime
from kubernetes import client, config
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
from pathlib import Path
from fastapi.responses import PlainTextResponse, FileResponse

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
log_directory = "/home/ubuntu/contMigration_logs"

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

@app.post("/migrate")
async def migrate_pod(request: Request):
    body = await request.json()
    print(f"Request body: ", body)
    #Currently source and target are not used because migration is always from cluster1 to cluster2
    source_cluster = body.get("source_cluster")
    target_cluster = body.get("target_cluster")
    
    pod_name = body.get("pod_name")
    print(f"Pod name", pod_name)
    #TODO: Implement the logic to generate forensic report and AI suggestions
    generate_forensic_report = body.get("forensic_analysis")
    generate_AI_suggestion = body.get("AI_suggestion")

    return await trigger_migration(pod_name)

def set_active_cluster(targetCluster: str):
    global activeClient
    if targetCluster == 'cluster1':
        activeClient = client1
    elif targetCluster == 'cluster2':
        activeClient = client2
    else: 
        raise ValueError(f"Invalid client choice: {client_choice}")


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    def create_node(name, path, is_file):
        node = {
            "label": name,
            "data": path.replace(rootdir, "").lstrip("/"),
            "expandedIcon": "pi pi-folder-open" if not is_file else "pi pi-file",
            "collapsedIcon": "pi pi-folder" if not is_file else "pi pi-file",
        }
        if not is_file:
            node["children"] = []
        return node

    def add_children(node, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if item == "temp":
                continue
            if os.path.isdir(item_path):
                child_node = create_node(item, item_path, False)
                add_children(child_node, item_path)
                node["children"].append(child_node)
            else:
                node["children"].append(create_node(item, item_path, True))

    root_node = {"children": []}
    add_children(root_node, rootdir)
    return root_node["children"]    

@app.get("/directory-structure")
async def directory_structure():
    log_directory = "/home/ubuntu/contMigration_logs"  # Replace with your directory path
    directory_structure = get_directory_structure(log_directory)
    return {"data": directory_structure}

@app.get("/view/{file_path:path}")
async def get_file_content(file_path: str):
    try:
        # Resolve the full path of the requested file
        root_path = Path(log_directory).resolve()
        requested_file = (root_path / file_path).resolve()

        # Ensure the requested file is within the allowed directory
        if not requested_file.is_file() or root_path not in requested_file.parents:
            raise HTTPException(status_code=404, detail="File not found or access denied")

        if requested_file.suffix != ".txt":
            raise HTTPException(status_code=400, detail="Only text files are allowed")

        # Read and return the content of the file
        with requested_file.open("r", encoding="utf-8") as file:
            content = file.read()

        return {"content": content}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    try:
        # Resolve the full path of the requested file
        root_path = Path(log_directory).resolve()
        requested_file = (root_path / file_path).resolve()

        # Ensure the requested file is within the allowed directory and is a .txt file
        if not requested_file.is_file() or root_path not in requested_file.parents :
            raise HTTPException(status_code=404, detail="File not found or access denied")

        if requested_file.suffix != ".txt":
            raise HTTPException(status_code=400, detail="Only text files are allowed")

        # Return the file for download
        return FileResponse(requested_file, media_type='application/octet-stream', filename=requested_file.name)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("migration:app", host="0.0.0.0", port=8000, reload=True)
