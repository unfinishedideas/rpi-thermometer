# https://www.freva.com/dht11-temperature-and-humidity-sensor-on-raspberry-pi/

import csv
import time
from datetime import datetime

SLEEP = 2.0

with open('test.csv', 'w', newline='') as csvfile:
    headerList = ['date', 'time', 'temp c', 'temp f', 'humidity %']
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(headerList)

while True:
    try:
        with open('test.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            now = datetime.now()
            temp_c = 32
            temp_f = 0
            humidity = 20
            writer.writerow([f'{now.year}/{now.month}/{now.day}', f'{now.hour}:{now.minute}', '100', '200', '30'])

        print(f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute} | Temperature {temp_c}*C {temp_f}*F Humidity: {humidity}%")
        csvfile.close()
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(SLEEP)
        continue
    except Exception as error:
        # sensor.exit()
        raise error
    time.sleep(SLEEP)
