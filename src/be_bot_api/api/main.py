from fastapi import FastAPI
from fastapi.responses import HTMLResponse
 
app = FastAPI()
 
@app.get("/")
def read_root():
    html_content = "<h2>I am TIM!</h2>"
    return HTMLResponse(content=html_content)

@app.get("/devices")
def read_all_devices():
    return {"name": "device1"}