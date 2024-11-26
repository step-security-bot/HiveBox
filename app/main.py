from fastapi import FastAPI
from endpoints import version, temperature

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/version")
async def get_version():
    app_version = version.list_version()
    return {f"Version: {app_version}"}

@app.get("/temperature")
async def get_temperature():
    data = await temperature.avg_temperature()
    return data