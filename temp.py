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

SLEEP = 900

# Write the headers for the columns
with open('temps.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(['date', 'time', 'temp c', 'temp f', 'humidity %'])

while True:
    try:
        temp_c = sensor.temperature
        temp_f = (temp_c - 32) * (5/9)
        humidity = sensor.humidity
        print("Temperature: {}*C  {}*F  Humidity: {}% ".format(temp_c, temp_f, humidity))
        with open('temps.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            now = datetime.now()
            writer.writerow([f'{now.year}/{now.month}/{now.day}', f'{now.hour}:{now.minute}:{now.second}', f'{temp_c}', f'{temp_f}', f'{humidity}', '\n'])

        csvfile.close()
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(SLEEP)
        continue
    except Exception as error:
        sensor.exit()
        csvfile.close()
        raise error
    time.sleep(SLEEP)