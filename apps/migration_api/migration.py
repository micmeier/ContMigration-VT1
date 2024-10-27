from fastapi import FastAPI, HTTPException, Request
import subprocess

app = FastAPI()

ruleToTriggerMigration = [
    'Read sensitive file untrusted'
]

@app.post("/trigger-migration/")
async def handle_warning(request: Request):
    body = await request.json()
    hostname = body.get("hostname")
    rule = body.get("rule")
    priority = body.get("priority")
    k8s_pod_name = body.get("output_fields", {}).get("k8s.pod.name")

    if rule in ruleToTriggerMigration:
        print(f"Security event with priority {priority}and rule {rule} received from {hostname}")
        print(f"Migrating pod {k8s_pod_name} to a secure cluster")
        return await trigger_migration()


async def trigger_migration(k8s_pod_name):
    try:
        # Run the migration script located at /host/migration.sh
        #result = subprocess.run(["/home/ubuntu/ContMigration/scripts/migration/single-migration.sh"], check=True, capture_output=True, text=True)
        result = subprocess.run(["../../scripts/migration/single-migration.sh", k8s_pod_name], check=True, capture_output=True, text=True)

        # Return the result of the script execution
        return {"message": "Migration script executed successfully", "output": result.stdout}

    except subprocess.CalledProcessError as e:
    # Handle errors if the script fails
        raise HTTPException(status_code=500, detail=f"Error executing script: {e.stderr}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
