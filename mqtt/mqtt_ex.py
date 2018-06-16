import paho.mqtt.client as mqtt
import ssl
import json
import time
import logging
import random

# Mqtt Settings
mqtt_endpoint = 'mqtt.preview.oltd.de' 
connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    logging.debug("Connected with flags [%s] rtn code [%d]", flags, rc)
    if rc == 0:
      logging.debug("Connection Succesful")
      connected = True

def on_disconnect(client, userdata, rc):
    logging.debug("disconnected with rtn code [%d]", rc)

def on_publish(client, userdata, msgID):
    logging.debug("Published with MsgID [%d]", msgID)

logging.basicConfig(level=logging.DEBUG)

client = mqtt.Client('my-device_%d' % (random.randint(0, 1024)))
client.enable_logger()
client.on_connect = on_connect
client.on_diconnect = on_disconnect
client.on_publish = on_publish

client.tls_set(ca_certs='chain.pem', certfile='device_cert.pem', keyfile='device_key.pem', cert_reqs=ssl.CERT_REQUIRED,
   tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(True)
res = client.connect(mqtt_endpoint, 8883, 60)
logging.debug("Connect Results %d", res)

client.loop_start()

while connected == False:
    logging.debug("Waiting for connection")
    time.sleep(0.1)

logging.debug('Connected')

while True:
  # Publish Data on MQTT
  logging.debug('Publishing Data on MQTT')

  client.publish('data-ingest', json.dumps({
    'type': 'attributes',
    'value': {
      'temperature': random.randrange(0, 30)
    }
  }))
  logging.debug('Published')
  time.sleep(5)

client.disconnect()
client.loop_stop()
