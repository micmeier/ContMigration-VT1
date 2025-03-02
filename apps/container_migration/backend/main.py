from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app_routes import logs, k8s, migration, config, simulation

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

app.include_router(migration.router, prefix="", tags=["Migrations"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(k8s.router, prefix="/k8s", tags=["Kubernetes"])
app.include_router(config.router, prefix="/config", tags=["Configuration"])
app.include_router(simulation.router, prefix="/simulate", tags=["Attack Simulation"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)