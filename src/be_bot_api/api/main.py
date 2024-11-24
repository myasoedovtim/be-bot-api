from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
        title="bebot",
        version="1.0.0"
    )
 
@app.get("/")
def read_root():
    return ({"hello": "i'm bebot"})

@app.get("/devices")
def read_all_devices():
    return {"name": "device1"}