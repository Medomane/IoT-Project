import datetime
from storeData import DatabaseManager
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib import style
import matplotlib.ticker as plticker
from matplotlib.gridspec import GridSpec

style.use('fast')
font = {'family' : 'sans-serif',
        'size'   : 12}

dbObj = DatabaseManager()

fig = plt.figure()
gs = GridSpec(2, 3, figure=fig)
fig.canvas.set_window_title('Graphes')
ax1 = fig.add_subplot(gs[0, :2])
ax2 = fig.add_subplot(gs[1, :2])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 2])

def animate(i):
    #Temp
    tempData = dbObj.select_db_record("SELECT * FROM Temperature_Data ORDER BY Date_Time DESC LIMIT 20",[])

    xs = []
    ys = []

    for i in range( len(tempData) - 1, -1, -1):
        row = tempData[i]
        date_obj = datetime.datetime.strptime(row[2], '%d-%b-%Y %H:%M:%S:%f')
        xs.append(date_obj.time().strftime("%H:%M:%S"))
        ys.append(row[3])
    pass

    ax1.clear()
    ax1.set_title('Temperature overtime',**font)
    ax1.set_xlabel('Time',**font)
    ax1.set_ylabel('Temperature °C',**font)
    ax1.plot(xs, ys, color='tab:red')

    #Humidity
    HumidityData = dbObj.select_db_record("SELECT * FROM Humidity_Data ORDER BY Date_Time DESC LIMIT 20",[])

    xs = []
    ys = []

    for i in range( len(HumidityData) - 1, -1, -1):
        row = HumidityData[i]
        date_obj = datetime.datetime.strptime(row[2], '%d-%b-%Y %H:%M:%S:%f')
        xs.append(date_obj.time().strftime("%H:%M:%S"))
        ys.append(row[3])
    pass

    ax2.clear()
    ax2.set_title('Humidity overtime',**font)
    ax2.set_xlabel('Time',**font)
    ax2.set_ylabel("Humidity %rh",**font)
    ax2.plot(xs, ys)
    #-------------------------------------------------------------------------------------------------------------------------------------------
    #Temp pie chart
    tempLevels = dbObj.select_db_record("SELECT TemperatureLevel, count(SensorID) FROM Temperature_Data GROUP BY TemperatureLevel", [])
    labels = []
    sizes = []
    for row in tempLevels:
        labels.append(row[0])
        sizes.append(row[1])
    ax3.clear()
    ax3.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax3.axis('equal')

    #Humidity pie chart
    tempLevels = dbObj.select_db_record("SELECT HumidityLevel, count(SensorID) FROM Humidity_Data GROUP BY HumidityLevel", [])
    labels = []
    sizes = []
    for row in tempLevels:
        labels.append(row[0])
        sizes.append(row[1])
    ax4.clear()
    ax4.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax4.axis('equal')

    fig.autofmt_xdate()
    fig.tight_layout()
    
ani1 = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()