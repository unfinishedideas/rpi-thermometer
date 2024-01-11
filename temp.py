# https://www.freva.com/dht11-temperature-and-humidity-sensor-on-raspberry-pi/

import csv
import time
import board
import adafruit_dht
import psutil
from datetime import datetime

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)

SLEEP = 300.0

# Write the headers for the columns
with open('temps.csv', 'w', newline='') as csvfile:
    headerlist = ['date', 'time', 'temp c', 'temp f', 'humidity %']
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(headerlist)
    while True:
        try:
            now = datetime.now()
            temp_c = sensor.temperature
            temp_f = (temp_c * (9/5)) + 32
            humidity = sensor.humidity
            writer.writerow([f'{now.year}/{now.month}/{now.day}', f'{now.hour}:{now.minute}:{now.second}', f'{temp_c}', f'{temp_f}', f'{humidity}', '\n'])
            print(f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute} | Temperature: {temp_c}*C {temp_f}*F | Humidity: {humidity}%")
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(SLEEP)
            continue
        except Exception as error:
            sensor.exit()
            csvfile.close()
            raise error
        time.sleep(SLEEP)