# https://www.freva.com/dht11-temperature-and-humidity-sensor-on-raspberry-pi/
#!/usr/bin/env python3

print("Starting temperature sensor readings")

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
with open('temps.csv', 'a', newline='') as csvfile:
    sniffer = csv.Sniffer()
    if not sniffer.has_header("date"):
        headerlist = ['date', 'time', 'temp c', 'temp f', 'humidity %']
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(headerlist)
    csvfile.close()

while True:
    try:
        # Write to CSV file
        with open('temps.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            now = datetime.now()
            temp_c = sensor.temperature
            temp_f = (temp_c * (9/5)) + 32
            humidity = sensor.humidity
            writer.writerow([f'{now.year}/{now.month}/{now.day}', f'{now.hour}:{now.minute}:{now.second}', f'{temp_c}', f'{temp_f}', f'{humidity}', '\n'])
            csvfile.close()

        # Write to log file and print to screen
        textlog = open("attic-log.txt", "a")
        log_string = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute} | Temperature: {temp_c}*C {temp_f}*F | Humidity: {humidity}%"
        textlog.write(f"{log_string}\n")
        textlog.close()
        print(log_string)

    except RuntimeError as error:
        # Errors happen often, re-read!
        print(error.args[0])
        time.sleep(1.0)
        continue
    except Exception as error:
        sensor.exit()
        csvfile.close()
        raise error
    time.sleep(SLEEP)