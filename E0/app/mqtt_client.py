import paho.mqtt.client as mqtt
import json
from .database import save_stock

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "stocks/info"

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        stock_data = json.loads(payload)

        if all(key in stock_data for key in ["symbol", "price", "shortName", "longName", "quantity", "timestamp"]):
            save_stock(stock_data)
            print(f"Nuevo stock recibido: {stock_data}")
        else:
            print(f"Mensaje MQTT con formato inválido: {payload}")
    except Exception as e:
        print(f"Error al procesar el mensaje MQTT: {e}")

def connect_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Conectado al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}")
    client.subscribe(MQTT_TOPIC)
    print(f"Suscrito al canal: {MQTT_TOPIC}")
    client.loop_start()
    return client

if __name__ == "__main__":
    mqtt_client = connect_mqtt()