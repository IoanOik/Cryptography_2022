#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time

class bs_receiver:
    def __init__(self, client_name):
        self.broker_address = "127.0.0.1"
        self.topic = "ack_messages"
        self.client = mqtt.Client(client_name)
        self.client.connect(self.broker_address)
        self.client.subscribe(self.topic)


def scan_msg(msg, id_new):
    id = msg[0]
    if id_new == id:
        if msg[1] == 0:
            print("Message has been accepted from the spacecraft with id -> " + str(id))
        else:
            print(
                "Message has  been rejected from the spacecraft with id -> " + str(id)
            )


def on_message(clent, userdata, message):
    print("Received: " + str(message.payload))
    # received_messages.append(message)


#spacecraft_id = int(input("Give id of the targeted spacecraft: "))
base_station_rcvr = bs_receiver("base_station")
base_station_rcvr.client.loop_start()
base_station_rcvr.client.on_message = on_message
time.sleep(20)
base_station_rcvr.client.loop_stop()
