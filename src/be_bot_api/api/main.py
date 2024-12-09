from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi_mqtt import FastMQTT, MQTTConfig
from dotenv import dotenv_values
from be_bot_api.api.device import Device

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

devices = []
devices.append(Device("guid1","TestDevice1","HomeRobot", True, ["Forward", "Backward"], ["Distans"]))

@app.on_event("startup")
async def startapp():
    await mqtt.connection()

@app.on_event("shutdown")
async def shutdown():
    await mqtt.client.disconnect()

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected to mqtt: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

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

@app.post("/bebot/api/v1.0/device")
def add_device(data = Body()):
    devices.append(Device(data["id"], data["name"], data["type"], data["status"], data["actions"], data["sensors"]))
    return devices

@app.get("/bebot/api/v1.0/test/send_mqtt_message")
async def send_mqtt_message():
    mqtt.publish("/mqtt", "Hello from Fastapi")
    return {"result": True,"message":"Published" }

