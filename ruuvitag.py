import time
import json
import random
import paho.mqtt.client as mqtt
from threading import Timer
from ruuvitag_sensor.ruuvi import RuuviTagSensor


MQTTHOST = "mqtt.preview.oltd.de"
MQTTPORT = 8883


client = mqtt.Client('rpi-gateway_%d' % (random.randint(0, 1024)))
client.tls_set(ca_certs='chain.pem', certfile='device_cert.pem', keyfile='device_key.pem')

def on_mqtt_log(client, userdata, level, buf):
    print(client, userdata, level, buf)

def on_mqtt_connect(client, userdata, flags, rc):
    print("Connected to MQTT server {} with result code {} ({}).".format(MQTTHOST, mqtt.connack_string(rc), rc))

def on_mqtt_disconnect(client, userdata, rc):
    print("Disconnected with code {} ({})".format(mqtt.connack_string(rc), rc))

def on_mqtt_message(client, userdata, msg):
    print("Got: " + msg.topic+" "+str(msg.payload))


def push_data_ruuvitag():
    msg = {
            "type": "attributes",
            "value": {
                "temperature": 17,
                "pressure": 16,
                "humidity": 15,
                "battery": 14,
                "acceleration": {
                    "x": 10,
                    "y": 9,
                    "z": 8
                }
            }
          }
    print(client.publish("data-ingest", payload=json.dumps(msg).encode('UTF-8')))
    print(msg)
    t = Timer(2, push_data_ruuvitag)
    t.start()


client.on_connect = on_mqtt_connect
client.on_message = on_mqtt_message
client.on_disconnect = on_mqtt_disconnect
client.on_log = on_mqtt_log
client.connect_async(MQTTHOST, MQTTPORT)

client.loop_start()

t = Timer(2, push_data_ruuvitag)
t.start()

while True:
    time.sleep(1)
