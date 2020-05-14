#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3

#SQLite DB Name
DB_NAME = "IoT_DataBase.db"

#===========================================================
#Database Manager Class

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur =  self.conn.cursor()
        
    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return
    
    def select_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return self.cur.fetchall()
    
    def __del__(self):
        self.cur.close
        self.conn.close
    
    @staticmethod
    def getDataSet(sqlText):
        #Push into DB Table
        dbObj = DatabaseManager()
        rows = dbObj.select_db_record(sqlText)
        del dbObj
        return rows
    

#===========================================================
# Functions to push sensor Data intro Database
        
# Functions to save Temperature to DB Table
def Temperature_Data_Handler(jsonData):
    #Parse Data
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Date_Time = json_Dict['Date']
    Temperature = float(json_Dict['Temperature'])
    TemperatureLevel = json_Dict['TemperatureLevel']
    
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Temperature_Data(SensorID, Date_Time, Temperature, TemperatureLevel) values (?, ?, ?, ?)",[SensorID, Date_Time, Temperature, TemperatureLevel])
    del dbObj
    print('Inserted Temperature Data into Database')
    print('')
    
# Functions to save Humidity to DB Table
def Humidity_Data_Handler(jsonData):
    print('test ', jsonData)
    #Parse Data
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Date_Time = json_Dict['Date']
    Humidity = float(json_Dict['Humidity'])
    HumidityLevel = json_Dict['HumidityLevel']
    print('test ', SensorID, Date_Time, Humidity, HumidityLevel)
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Humidity_Data(SensorID, Date_Time, Humidity, HumidityLevel) values (?, ?, ?, ?)",[SensorID, Date_Time, Humidity, HumidityLevel])
    del dbObj
    print('Inserted Humidity Data into Database')
    print('')
    
# Functions to save Acceleration to DB Table
def Acceleration_Data_Handler(jsonData):
    #Parse Data
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Date_Time = json_Dict['Date']
    print('********** ', Date_Time)
    accX = float(json_Dict['accX'])
    accY = float(json_Dict['accY'])
    accZ = float(json_Dict['accZ'])
    
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Acceleration_Data(SensorID, Date_Time, accX, accY, accZ) values (?, ?, ?, ?, ?)",[SensorID, Date_Time, accX, accY, accZ])
    del dbObj
    print('Inserted Acceleration Data into Database')
    print('')
    
#===========================================================
# Master Function to select DB function based on MQTT Topic
def sensor_Data_Handler(Topic, jsonData):
    if Topic == 'Home/BedRoom/DHT1/Temperature':
        Temperature_Data_Handler(jsonData)
    elif Topic == 'Home/BedRoom/DHT1/Humidity':
        Humidity_Data_Handler(jsonData)
    elif Topic == 'Home/BedRoom/DHT1/Acceleration':
        Acceleration_Data_Handler(jsonData)

#===========================================================