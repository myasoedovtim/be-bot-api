from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mqtt import FastMQTT, MQTTConfig
from dotenv import dotenv_values
from be_bot_api.api.device import Device
import jsonpickle

# Загрузка переменных окружения.
env_vars = dotenv_values(".env")   

app = FastAPI(
        title=env_vars.get("APP_NAME"),
        version=env_vars.get("APP_VERSION")
    )

mqtt_config = MQTTConfig()
mqtt_config.host = env_vars.get("MQTT_HOST")
mqtt_config.port = env_vars.get("MQTT_PORT")
mqtt_config.username = env_vars.get("MQTT_USER")
mqtt_config.password = env_vars.get("MQTT_PASSWORD")

mqtt = FastMQTT(
    config=mqtt_config
)


devices = {}

@app.on_event("startup")
async def startapp():
    await mqtt.connection()

@app.on_event("shutdown")
async def shutdown():
    await mqtt.client.disconnect()

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/bebot/to/api/init")
    mqtt.client.subscribe("/bebot/to/api/status")
    print("Connected to mqtt: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    device = jsonpickle.decode(payload.decode())
    print(device)
    if(topic=="/bebot/to/api/init" and device["device_id"] not in devices):
        devices[device["device_id"]] = device
    if(topic=="/bebot/to/api/status" and device["device_id"] in devices):
        devices[device["device_id"]]["is_active"] = device["is_active"]
    


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected from mqtt")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)
 
@app.get("/")
def read_root():
    return ({"hello": "i'm bebot!"})

@app.get("/bebot/api/v1.0/devices")
def get_devices():
    return devices

@app.post("/bebot/api/v1.0/devices", status_code=status.HTTP_201_CREATED)
def add_device(device : Device):
    if device.device_id in devices:
        raise HTTPException(status_code=400, detail="Device already exists")
    devices[device.device_id] = device
    return device

@app.get("/bebot/api/v1.0/devices/{device_id}", response_model=Device)
async def get_device(device_id: str):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices[device_id]

@app.get("/bebot/api/v1.0/command/forward/{device_id}/{value}")
async def send_command_forward(device_id: str, value: int):
    if device_id in devices:
        mqtt.publish("/bebot/device/"+device_id, {"forward": value})
    else:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"detail": "Ok"}

@app.get("/bebot/api/v1.0/command/backward/{device_id}/{value}")
async def send_command_backward(device_id: str, value: int):
    if device_id in devices:
        mqtt.publish("/bebot/device/"+device_id, {"backward": value})
    else:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"detail": "Ok"}

@app.get("/bebot/api/v1.0/command/getsensor/{device_id}")
async def send_command_backward(device_id: str, sensor_type: str):
    if device_id in devices:
        mqtt.publish("/bebot/device/"+device_id, {"getsensor": sensor_type})
    else:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"detail": "Ok"}
