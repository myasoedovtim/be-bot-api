from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_mqtt import FastMQTT, MQTTConfig
from dotenv import dotenv_values

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
 
@app.get("/")
def read_root():
    return ({"hello": "i'm bebot"})

@app.get("/devices")
def read_all_devices():
    return {"name": "device1"}