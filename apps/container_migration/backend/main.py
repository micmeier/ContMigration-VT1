from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routesTest import logs, k8s, migration

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

app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(k8s.router, prefix="/k8s", tags=["Kubernetes"])
app.include_router(migration.router, prefix="", tags=["Migrations"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)