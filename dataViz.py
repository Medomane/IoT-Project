import datetime
from storeData import DatabaseManager
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib import style
import matplotlib.ticker as plticker
style.use('fivethirtyeight')

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

fig2, (ax3, ax4) = plt.subplots(nrows=2, ncols=1)

dbObj = DatabaseManager()

loc = plticker.MultipleLocator(base=1.5)

def animate(i):
    #Temp
    tempData = dbObj.select_db_record("SELECT * FROM Temperature_Data ORDER BY Date_Time DESC LIMIT 20",[])
    print(tempData)

    xs = []
    ys = []

    for i in range( len(tempData) - 1, -1, -1):
        row = tempData[i]
        date_obj = datetime.datetime.strptime(row[2], '%d-%b-%Y %H:%M:%S:%f')
        print(date_obj)
        print(row[2]) #extract date
        print(row[3]) #extract temp value
        xs.append(date_obj.time().strftime("%H:%M:%S"))
        ys.append(row[3])
    pass

    ax1.clear()
    ax1.set_title('Temperature overtime')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature °C')
    ax1.plot(xs, ys, color='tab:red')
    ax1.xaxis.set_major_locator(loc)
    #Humidity

    HumidityData = dbObj.select_db_record("SELECT * FROM Humidity_Data ORDER BY Date_Time DESC LIMIT 20",[])
    print(HumidityData)

    xs = []
    ys = []

    for i in range( len(HumidityData) - 1, -1, -1):
        row = HumidityData[i]
        date_obj = datetime.datetime.strptime(row[2], '%d-%b-%Y %H:%M:%S:%f')
        print(date_obj)
        print(row[2]) #extract date
        print(row[3]) #extract Humidity value
        xs.append(date_obj.time().strftime("%H:%M:%S"))
        ys.append(row[3])
    pass

    ax2.clear()
    ax2.set_title('Humidity overtime')
    ax2.set_xlabel('Time')
    ax2.set_ylabel("Humidity %rh")
    ax2.plot(xs, ys)
    ax2.xaxis.set_major_locator(loc)
    

    #Temp pie chart
    tempLevels = dbObj.select_db_record("SELECT TemperatureLevel, count(SensorID) FROM Temperature_Data GROUP BY TemperatureLevel", [])
    labels = []
    sizes = []
    for row in tempLevels:
        labels.append(row[0])
        sizes.append(row[1])
    print(labels)
    print(sizes)
    ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax3.axis('equal')

    #Humidity pie chart
    tempLevels = dbObj.select_db_record("SELECT HumidityLevel, count(SensorID) FROM Humidity_Data GROUP BY HumidityLevel", [])
    labels = []
    sizes = []
    for row in tempLevels:
        labels.append(row[0])
        sizes.append(row[1])
    print(labels)
    print(sizes)
    ax4.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax4.axis('equal')


    fig.autofmt_xdate()
    plt.tight_layout()
    plt.xticks(rotation=65, ha='right')
    


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()