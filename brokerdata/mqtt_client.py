import paho.mqtt.client as mqtt
import os
import django
import logging
from brokerdata.models import SensorData  # Ensure this import matches your project structure

# Initialize Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensordata.settings")
django.setup()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define MQTT settings
MQTT_BROKER = "100.29.71.194"  # Adjust IP as needed
MQTT_PORT = 1883
MQTT_TOPICS = ["sensor1", "sensor2"]

def on_connect(client, userdata, flags, rc):
    logging.debug(f"Connected with result code {rc}")
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
        logging.debug(f"Subscribed to topic {topic}")

def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode()
        topic = msg.topic
        logging.debug(f"Received message on topic {topic}: {data}")

        # Save to database
        SensorData.objects.create(topic=topic, data=data)
        logging.debug(f"Data saved for topic {topic}: {data}")
    except Exception as e:
        logging.error(f"Error saving data: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt_client():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

start_mqtt_client()
