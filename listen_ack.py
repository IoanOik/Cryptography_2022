#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time

received_messages = []

class bs_receiver:
    def __init__(self, client_name):
        self.broker_address = "127.0.0.1"
        self.topic = "ack_messages"
        self.client = mqtt.Client(client_name)
        self.client.on_connect = on_connect
        self.client.connect(self.broker_address)
        self.client.subscribe(self.topic)


def on_connect(client, userdata, flags, rc):
    print("Connection succesfull" if rc == 0 else "Connection failed")
    print(
        "Connection status: " + str(rc)
    )  # we happy when that is 0, else we must visit the documentation to recognize the error code


def scan_msg(msg):
    id = msg[0]
    if msg[1] == 0:
        print("Message has been accepted from the spacecraft with id -> " + str(id))
    else:
        print("Message has been rejected from the spacecraft with id -> " + str(id))


def on_message(clent, userdata, message):
    print("On message executing...")
    print("Received: " + str(message.payload))
    received_messages.append(message)


base_station_rcvr = bs_receiver("base_station")
base_station_rcvr.client.on_message = on_message
base_station_rcvr.client.loop_start()
time.sleep(3)
base_station_rcvr.client.loop_stop()
base_station_rcvr.client.disconnect()
for msg in received_messages:
    scan_msg(msg.payload)
