from django.shortcuts import render
from django.http import HttpResponse
import csv
from .models import SensorData
from rest_framework.views import APIView
from rest_framework.response import Response
import paho.mqtt.client as mqtt
import logging

MQTT_BROKER = "100.29.71.194"  # Adjust IP as needed
MQTT_PORT = 1883
MQTT_TOPICS = ["sensor1", "sensor2"]

def index(request):
    topics = SensorData.objects.values_list('topic', flat=True).distinct()
    topic_location_mapping = {
        'sensor1': 'location1',
        'sensor2': 'location2'
    }
    topics_with_locations = [{'topic': topic, 'location': topic_location_mapping.get(topic)} for topic in topics]
    return render(request, 'index.html', {'topics_with_locations': topics_with_locations})

class ChartData(APIView):
    def get(self, request, topic, format=None):
        try:
            data = SensorData.objects.filter(topic=topic).values('timestamp', 'data')
            return Response(list(data))
        except Exception as e:
            logging.error(f"Error fetching data for topic {topic}: {e}")
            return Response({"error": "Failed to fetch data"}, status=500)

def download_csv(request, topic):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{topic}_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Data'])

    for row in SensorData.objects.filter(topic=topic).values_list('timestamp', 'data'):
        writer.writerow(row)

    return response

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
