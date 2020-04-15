import json

import paho.mqtt.client as mqtt
import time

from src.file_paths import PathConsts


class MqttClient:
    def __init__(self, ip, port, topic=None):
        self.client = mqtt.Client()
        self.client.connect(ip, port, 60)

        if topic:
            self.subscribe_to(topic)

        self.__state_filename = '../resources/state.txt'
        self.__color_filename = '../resources/color.txt'

    def on_message(self, message):
        message = json.loads(str(message.payload.decode("utf-8")))

        if 'state' in message:
            res_file = open(PathConsts.state_filename, mode="w+", encoding="utf-8")
            msg_to_write = ''

            if message['state'] == 'true':
                msg_to_write = 'True'
            elif message['state'] == 'false':
                msg_to_write = 'False'

            res_file.write(msg_to_write)
        elif 'color' in message:
            res_file = open(PathConsts.color_filename, mode="w+", encoding="utf-8")

            msg_to_write = ""
            color = message['color']
            for c in color:
                msg_to_write += str(c) + " "

            res_file.write(str.strip(msg_to_write))
        else:
            print("Incorrect data received:", end=" ")
            print(message)

    def subscribe_to(self, topic):
        self.client.subscribe(topic)
        time.sleep(2)

    def get_client(self):
        return self.client

    def destruct(self):
        self.client.disconnect()


mqtt_client = MqttClient("10.10.0.15", 1883, "iot/project")
mqtt_client.get_client().on_message = mqtt_client.on_message
mqtt_client.get_client().loop_start()
