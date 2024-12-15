from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
import subprocess
import os

app = FastAPI()

ruleToTriggerMigration = [
    'Read sensitive file untrusted',
    'Drop and execute new binary in container',
    'Redirect STDOUT/STDIN to Network Connection in Container'
]
triggeredMigrations = []

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
