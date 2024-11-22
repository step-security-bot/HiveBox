from fastapi import FastAPI
from endpoints import version

app = FastAPI()

@app.get("/version")
async def get_version():
    app_version = version.list_version()
    return {f"Version: {app_version}"}

@app.get("/")
async def root():
    return {"message": "Hello World"}