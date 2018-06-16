# -*- coding: utf-8 -*-
#! /usr/bin/env python3

"""
Created on Wed Feb 28 17:42:25 2018

@author: C.Mair2
"""

import json
import os
import requests
import subprocess
import datetime

#DOMAIN='api.lightelligence.io'
DOMAIN='api.preview.oltd.de'
#tenant_id="1"


URL = {}
URL['base'] =       'https://'+DOMAIN+'/v1'
URL['tenant'] =     URL['base'] + '/tenants'
URL['devicetype'] = URL['base'] + '/device-types'
URL['device'] =     URL['base'] + '/devices'


# Auth token
AUTH_TOKEN=''


###
# Create/POST an object in OLT and parse result into json.
#
def create_request(url, auth, payload):
    print("Connecting to {}".format(url))
#    print("Create {}".format(payload))
    result = requests.post(url, headers={'Authorization': 'Bearer ' + auth, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}, json=payload, verify=False)
    if result.reason == 'Created' or result.reason == 'OK':
        if "application/json" in result.headers['Content-Type']:
            return json.loads(result.content.decode("UTF-8"))
        else:
            print(result.content)
            return result.content
    else:
        print(result.content)
        return None

###
# Request an object from OLT
#
def get_response(url, auth):
    print("Connecting to {}".format(url))
    result = requests.get(url, headers={'Authorization': 'Bearer ' + auth, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}, verify=False)
    if result.reason == 'OK':
        if "application/json" in result.headers['Content-Type']:
            return json.loads(result.content.decode("UTF-8"))
        else:
            return result.content
    else:
        print("ERROR: {}".format(result.content))
        return None


###
# Try to fetch an object with specified ID from OLT.
# Return None if the ID was not found or does not match.
#
def get_object(url, id, auth):
    if len(id) > 0:
        print("Connecting to {}".format(url))
        result = get_response(url + '/' + id, AUTH_TOKEN)
        print(result)
        if result and "data" in result and result["data"].get("id") == id:
            return result["data"]
        else:
            return None
    else:
        return None


###
# Recursively sort any lists and convert dicts to lists of (key, value) pairs so they're orderable.
# For dicts, just consider keys which contain 'id' to only identify changes in the referenced objects
# instead of all properties
#
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items() if 'id' in k.lower())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

###
# Try to get an object from OLT. Create one, if not existing.
#
def create_or_get(name, cfg, url, auth, payload):
    print("\n-------- {} -------".format(name))
    id = cfg.get('id', "")
    obj = get_object(url[name], id, auth)
    created = False
    if ordered(obj) == ordered(cfg):
        print("Using existing {}: {}".format(name, id))
    else:
        obj = None
        result = create_request(url[name], auth, payload)
        if result:
            print("Created new {}: {}".format(name, result))
            if type(result['data']) == str:
                obj = json.loads(result['data'])
            elif type(result['data']) == dict:
                obj = result['data']
            else:
                print("\nSEVERE API ERROR: bogus return type!\n")
                quit()
            created = True
            if not obj:
                print("Could not create {}".format(name))
#    print(obj)
    return obj, created



path = os.path.dirname(os.path.realpath(__file__))
try:
    with open(path+'/config.json', 'r') as configfile:
        config = json.load(configfile)
except FileNotFoundError:
    print("Config file not found, creating a new one.")
    config = {}


#config['tenant'], created = create_or_get('tenant', config.get('tenant', {}), URL, AUTH_TOKEN,
#    {
#      "id": "a49e3b23-66eb-4d52-b761-5631b9241c44",
#    })

config['tenant'] = {
        "id": "a49e3b23-66eb-4d52-b761-5631b9241c44",
        "name": "Haus1"
    }

###
# Do not create a new role, as a already existing user and tenant id will be used.
#
#config['role'], created = create_or_get('role', config.get('role', {}), URL, AUTH_TOKEN,
#    {
#           # Musterfrau
##          "subjectId": "948e4969-11c4-43d9-b045-e24684cf1785",
#           # cmair2
#           "subjectId": "45852f63-6000-427a-8db6-995aacef7dfd",
#           # tkhun
##           "subjectId": "5a768a9b-97c5-4ca8-9e87-8f2035198bdf",
#           "subjectType": "user",
#           "targetId": config['tenant']['id'],
#           "targetType": "tenant",
#           "permissionLevel": "admin"
#    })
#

if not 'devicetype' in config:
    config['devicetype'] = {}


config['devicetype']['ruuvitag'], created = create_or_get('devicetype', config.get('devicetype', {}).get('ruuvitag', {}), URL, AUTH_TOKEN,
    {
        "name": "RuuviTag",
        "description": "BLE Sensor Beacon",
        "manufacturer": "Ruuvi",
        "model": "RuuviTag",
        "schema": {
            "attributes": {
                "temperature": { "type": "number" },
                "pressure": { "type": "number" },
                "humidity": { "type": "number" },
                "battery": { "type": "number" },
                "acceleration": {
                     "type": "object",
                     "properties": {
                         "x": { "type": "number" },
                         "y": { "type": "number" },
                         "z": { "type": "number" }
                     }
                }
            },
            "configuration": {
            }
        },
        "reportingRules": [
            {
                "path": "$.attributes.temperature",
                "reportTo": [
                    "timeseries"
                ]
            },
            {
                "path": "$.attributes.pressure",
                "reportTo": [
                    "timeseries"
                ]
            },
            {
                "path": "$.attributes.humidity",
                "reportTo": [
                   "timeseries"
                ]
            },
            {
                "path": "$.attributes.battery",
                "reportTo": [
                    "timeseries"
                ]
            },
            {
                "path": "$.attributes.acceleration.x",
                "reportTo": [
                    "timeseries"
                ]
            },
            {
                "path": "$.attributes.temperature.y",
                "reportTo": [
                    "timeseries"
                ]
            },
            {
                "path": "$.attributes.temperature.z",
                "reportTo": [
                    "timeseries"
                ]
            },
        ]
    })


config['devicetype']['peoplecounter'], created = create_or_get('devicetype', config.get('devicetype', {}).get('peoplecounter', {}), URL, AUTH_TOKEN,
    {
        "name": "Peoplecounter",
        "description": "Counts people and calculates relative coordinates",
        "manufacturer": "Generic",
        "model": "Generic",
        "schema": {
            "attributes": {
                "count": { "type": "number" },
                "coordinates": {
                     "type": "array",
                     "items": {
                         "x": { "type": "number" },
                         "y": { "type": "number" },
                     }
                }
            },
            "configuration": {
            }
        }
        "reportingRules": [
            {
                "path": "$.attributes.count",
                "reportTo": [
                    "timeseries"
                ]
            },
    })


if not 'device' in config:
    config['device'] = {}

config['device']['ruuvitag'], created = create_or_get('device', config.get('device', {}).get('ruuvitag', {}), URL, AUTH_TOKEN,
    {
        "info": {
            "name": "RuuviTag #1",
            "deviceTypeId": config['devicetype']['ruuvitag']['id'],
            "description": "BLE Sensor Beacon",
            "installationTimestamp": '2018-06-05T08:23:10.370Z',
            "tags": [ "ambient" ]
        },
        "attributes": {
            "temperature": 0,
            "pressure": 0,
            "humidity": 0,
            "battery": 0,
            "acceleration": {
                "x": 0,
                "y": 0,
                "z": 0,
            }
        }
    })


config['device']['grideye'], created = create_or_get('device', config.get('device', {}).get('grideye', {}), URL, AUTH_TOKEN,
    {
        "info": {
            "name": "GrideyeKompakt",
            "deviceTypeId": config['devicetype']['peoplecounter']['id'],
            "description": "GridEye Kompakt people counter",
            "installationTimestamp": '2018-06-05T08:23:10.370Z',
            "tags": [ "peoplecounter" ],
            "connectedBy": config['device']['ruuvitag']['id']
        },
        "attributes": {
            "count": 0,
            "coordinates": {
            }
        }
    })


path = os.path.dirname(os.path.realpath(__file__))
with open(path+'/config.json', 'w') as configfile:
    json.dump(config, configfile, indent=4, sort_keys=True)


# Create a new certificate only if the connector ID changed. In all other cases BAD THINGS™ will happen!
# You have been warned.
#if created_new_connector:
print("\nCreating certificate...")
subprocess.call("openssl ecparam -out device_key.pem -name prime256v1 -genkey", shell=True)
subprocess.call("openssl req -new -key device_key.pem -x509 -days 365 -out device_cert.pem -subj '/O={}/CN={}'".format(config['tenant']['id'], config['device']['ruuvitag']['id']), shell=True)

with open("device_cert.pem") as f:
    cert = "\n".join(line.strip() for line in f)

print(cert)

print("Register certificate..")
print(create_request(URL['device'] + "/{}/certificates".format(config['device']['ruuvitag']['id']), AUTH_TOKEN, {"cert": cert, "status": "valid"}))


print("------------------------------------------")
print("Here's what just happened:")
# print("Created role {} and assigned tenant {} to user {}".format(config['role']["id"], config['role']["targetId"], config['role']["subjectId"]))
# print("Created connector {}".format(config['connector']["id"]))
print("Created device {} with type {}".format(config['device']['ruuvitag']["id"], config['devicetype']["ruuvitag"]["id"]))
print("Created device {} with type {}".format(config['device']['grideye']["id"], config['devicetype']["peoplecounter"]["id"]))
print("Thats it!")
