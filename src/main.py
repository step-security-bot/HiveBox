from fastapi import FastAPI

from endpoints import temperature, version

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
    avg = await temperature.avg_temperature()
    return {f"Average temperature (°C): {avg}"}
