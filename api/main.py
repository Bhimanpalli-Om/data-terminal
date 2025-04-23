from fastapi import FastAPI, Request
from typing import Dict, Any

app = FastAPI()

nse_preopen_data = {}

@app.post("/preopen")
async def receive_preopen_data(request: Request):
    data = await request.json()
    global nse_preopen_data
    nse_preopen_data = data
    return {"status": "success", "message": "Data received"}

@app.get("/preopen")
def get_preopen_data():
    return nse_preopen_data