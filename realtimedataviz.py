#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from storeData import sensor_Data_Handler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
import json
from time import sleep
import random

plt.xkcd()
class SensorDataHandler():
    def __init__(self, data_length=20):
        self.values = []
        self.times = []
        self.level_values = []
        self.is_updated = False
        self.max_data_len = data_length


    def update_shit(self, timez, value,level):
        print("updating...")
        if len(self.values) >= self.max_data_len:
            self.values.pop(0)
            self.times.pop(0)
            self.level_values.pop(0)
        self.values.append(value)
        self.level_values.append(level)
        self.times.append(timez)
        self.is_updated = True

    def set_updated(self, paramBool):
        self.is_updated = paramBool

    def get_updated(self):
        return self.is_updated


# VARIABLES
fig, (ax_temp,ax_humidity) = plt.subplots(nrows=2,ncols=1)
fig2, (chart_temp,chart_humidity) = plt.subplots(nrows=2,ncols=1)
# fig, ax = plt.subplots()
temp_sensor_dh = SensorDataHandler()
humidity_sensor_dh = SensorDataHandler()
ax_temp.legend()
ax_temp.set_title('Temperature')
ax_temp.set_xlabel('time')
ax_temp.set_ylabel('temperature')
ax_humidity.legend()
ax_humidity.set_ylabel('humidity level')
ax_humidity.set_xlabel('time')
ax_humidity.set_title('Humidity')
chart_temp.clear()
chart_humidity.clear()
def update_dataviz():
    global temp_sensor_dh
    global humidity_sensor_dh
    global ax_temp
    global ax_humidity 

    if temp_sensor_dh.get_updated()==True:
        ax_temp.clear()
        ax_temp.set_xlabel('time')
        ax_temp.set_ylabel('temps')
        ax_temp.plot(temp_sensor_dh.times,temp_sensor_dh.values,label = "temperature")
        temp_sensor_dh.set_updated(False)
    
        tmp = np.array(temp_sensor_dh.level_values)
        unique_elements, counts_elements = np.unique(tmp, return_counts=True)
        chart_temp.clear()
        chart_temp.pie(counts_elements, labels=unique_elements, autopct='%1.1f%%',
        shadow=True, startangle=90)
        chart_temp.axis('equal')
    if humidity_sensor_dh.get_updated()==True:
        ax_humidity.clear()
        ax_humidity.set_xlabel('time')
        ax_humidity.set_ylabel('humidity')
        ax_humidity.plot(humidity_sensor_dh.times,humidity_sensor_dh.values,label = "Humidity")
        humidity_sensor_dh.set_updated(False)
        plt.pause(0.001)
        tmp = np.array(humidity_sensor_dh.level_values)
        unique_elements, counts_elements = np.unique(tmp, return_counts=True)
        chart_humidity.clear()
        chart_humidity.pie(counts_elements, labels=unique_elements, autopct='%1.1f%%',
        shadow=True, startangle=90)
        chart_humidity.axis('equal')
    plt.draw()
    plt.pause(0.001)





def update_data(topic, data):
    print("Update_data called on ", topic)
    json_data = json.loads(data)
    if topic == "Home/BedRoom/DHT1/Temperature":

        print("Updating temp with ",json_data['Temperature'])
        temp_sensor_dh.update_shit(json_data['Date'][-15:-7], json_data['Temperature'],json_data['TemperatureLevel'])
   
     

    elif topic == "Home/BedRoom/DHT1/Humidity":
        
        print("Updating Humidity with ",json_data['Humidity'])
        humidity_sensor_dh.update_shit(json_data['Date'][-15:-7], json_data['Humidity'],json_data['HumidityLevel'])
     
    else:
        print("nigga wat, we cant handle that shitty topic rn bru")


def on_connect(self,mosq, obj, rc):
    if rc == 0:
        print("connected")
 
        mqttc.subscribe(MQTT_Topic, 0)
    else:
        print("bad connection")


def on_message(mosq, obj, msg):

    topic = msg.topic
    print("MQTT Data Received...")
    print(topic)
    print(msg.payload)
    update_data(str(topic),msg.payload)
    update_dataviz()
    
   

    

def on_subscribe(mosq, obj, mid, granted_qos):
    pass








plt.ion()
plt.show()


# MQTT Settings
MQTT_Broker = "mqtt.eclipse.org"
MQTT_Port = 1883
Keep_Alive_Interval = 30
MQTT_Topic = "Home/BedRoom/#"
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Connect & subscribe
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe(MQTT_Topic, 0)
mqttc.loop_forever()  # Continue the network loop

