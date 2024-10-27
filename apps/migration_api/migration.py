from urllib.request import Request

from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.post("/trigger-migration/")
async def trigger_migration(request: Request):
    body = await request.json()
    print(body)

    try:
        # Run the migration script located at /host/migration.sh
        #result = subprocess.run(["/home/ubuntu/ContMigration/scripts/migration/single-migration.sh"], check=True, capture_output=True, text=True)
        result = subprocess.run(["../../scripts/migration/single-migration.sh", "nginx-7bf5d9d764-42gms"], check=True, capture_output=True, text=True)

        # Return the result of the script execution
        return {"message": "Migration script executed successfully", "output": result.stdout}

    except subprocess.CalledProcessError as e:
        # Handle errors if the script fails
        raise HTTPException(status_code=500, detail=f"Error executing script: {e.stderr}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
