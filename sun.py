import numpy as np
import matplotlib.pyplot as plt

month_power = [200,250,300,350,400,450,500,300,200,100,150,50]
sun_time_day = [4,4,5,6,6,7,7,7,6,6,5,5]

def display_sun():
    time_months = np.arange(1, len(month_power)+1)  # Array from 1 to 7 representing time (days)
        # Generate a plot
    plt.plot(time_months, month_power, marker='o', linestyle='-', color='r')
    plt.title('Sun over a year')
    plt.xlabel('month')
    plt.ylabel('Power (kWh)')
    plt.grid(True)
    plt.savefig('sun_year.png')
    plt.clf()

    # plt.show()
    for id_month in range (len(sun_time_day)):
        night = (24 -sun_time_day[id_month])
        night = int(night/2)
        sun_hours = [0]*(night)+[month_power[id_month]]*sun_time_day[id_month]+[0]*(night)
        if len(sun_hours)==23:
            sun_hours.append(0)
    
        time_hours = np.arange(1, len(sun_hours)+1)  # Array from 1 to 7 representing time (days)
        plt.plot(time_hours, sun_hours, marker='o', linestyle='-', color='r')
        plt.title('Sun over day in '+str(id_month)+'th month')
        plt.xlabel('hours')
        plt.ylabel('Power (kWh)')
        plt.grid(True)
        plt.savefig(str(id_month)+'.png')
        plt.clf()
        # plt.show()
display_sun()