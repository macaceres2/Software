import paho.mqtt.client as mqtt
import json
import threading
from .database import save_stock
from .config import settings


class MQTTClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Conectando al broker {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
            self.is_connected = True
            client.subscribe(settings.MQTT_TOPIC)
            print(f"En el tema: {settings.MQTT_TOPIC}")
        else:
            print("Error al conectar broker por código {rc}")

    def on_message(client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            print(f"Mensaje recibido: {payload}")
            stock_data = json.loads(payload)

            if all(key in stock_data for key in ["symbol", "price", "shortName", "longName", "quantity", "timestamp"]):
                save_stock(stock_data)
                print(f"Nuevo stock guardado: {stock_data["symbol"]} en ${stock_data["price"]}")
            else:
                print(f"Mensaje MQTT con formato inválido: {payload}")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON: {payload}")
        except Exception as e:
            print(f"Error al procesar el mensaje MQTT: {e}")

    def connect(self):
        self.connect_mqtt()
    
    def connect_mqtt(self):
        if self.client is not None:
            return
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Error al conectar al broker: {e}")

    def disconnect(self):
        if self.client is not None and self.is_connected == True:
            self.client.loopstop()
            self.client.disconnect()
            self.is_connected = False
            print("Desconectado del broker")

mqtt_client = MQTTClient()