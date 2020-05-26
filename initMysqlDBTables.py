import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='172.17.0.2',
        database='iot_database',
        user='yasser',
        password='yasser',
        use_pure=True,
        charset='utf8',
    ) 
    table1 = """
    drop table if exists Temperature_Data;
    create table Temperature_Data (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
        SensorID VARCHAR(255) NOT NULL,
        Date_Time VARCHAR(255) NOT NULL,
        Temperature decimal(6,2),
        TemperatureLevel VARCHAR(255) NOT NULL 
        );
    drop table if exists Humidity_Data ;
    create table Humidity_Data (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
        SensorID VARCHAR(255) NOT NULL,
        Date_Time VARCHAR(255) NOT NULL,
        Humidity decimal(6,2),
        HumidityLevel VARCHAR(255) NOT NULL 
    );
    drop table if exists Acceleration_Data ;
    create table Acceleration_Data (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
        SensorID VARCHAR(255) NOT NULL,
        Date_Time VARCHAR(255) NOT NULL,
        accX decimal(6,2), accY decimal(6,2), accZ decimal(6,2)
    );
    """
    cursor = connection.cursor()
    results = cursor.execute(table1, multi=True)
    for cur in results:
        print('cursor:', cur)
        if cur.with_rows:
            print('result:', cur.fetchall())
    print("Laptop Tables created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")