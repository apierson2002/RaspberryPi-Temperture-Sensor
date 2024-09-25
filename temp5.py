# HEADER#########################################################################
# ANDREW PIERSON's TEMPERATURE SENSOR PROGRAM
# FILENAME: temp5.py    #do not change (for startup service)
# DATE: 7/20/2024
# DESCRIPTION: This python script uses glob api to measure the
#               temperature of the walk-in cooler at the Shoals Shack. The
#               sensor is connected to a Raspberry Pi that uses the request api
#               to send a text to boss.
#
# Order some food here: www.theshoalsshack.com
#
# CODE##########################################
import os
import glob
import time
import requests
import random

key = '4fe42da8f34496088125c8dc4d60e7a531634374Yc0jCA3nbsDHbQRPafdlL9Glc'
phone = 3128909930
tempset = 41

# Load Modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sensor in the filesystem
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave'

# Read temperature from device
def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

# Read temperature and return in Celsius and Fahrenheit
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_f = round(temp_f, 2)
        return temp_c, temp_f

# Send text message
def send_text(phone, key, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone,
        'message': message,
        'key': key,
    })
    data = resp.json()
    return data

# Function to construct text messages
def text_builder(message_type, temp_f=None, quota=None, tempset=None):
    if message_type == 'high_temp':
        return f'Coach Bj, the walk-in is above {tempset}°F.\nTemp is: {temp_f}°F'
    elif message_type == 'still_high_temp':
        return f'It has been 20 minutes and the temperature is still {temp_f}°F!\n\nSomething could be wrong!!!'
    elif message_type == 'temp_normal':
        return f'The walk-in cooler is back to normal :) Temp: {temp_f}°F\nText quota remaining: {quota}'
    else:
        return 'Unknown message type'

# Control loop
quota = 0
while True:
    temp_c, temp_f = read_temp()
    print(f'Temperature: {temp_c}°C, {temp_f}°F')
    time.sleep(2)  # Sleep for 2 seconds
    if temp_f >= tempset:
        text = text_builder('high_temp', temp_f=temp_f, tempset=tempset)
        data = send_text(phone, key, text)
        quota = data.get('quotaRemaining', quota)
        count = 0
        while temp_f >= tempset:
            time.sleep(300)  # Sleep for 5 minutes
            count += 1
            temp_c, temp_f = read_temp()
            print(f'Temperature: {temp_c}°C, {temp_f}°F')
            if count == 4:
                text = text_builder('still_high_temp', temp_f=temp_f)
                data = send_text(phone, key, text)
        # Temperature is back to normal
        text = text_builder('temp_normal', temp_f=temp_f, quota=quota)
        data = send_text(phone, key, text)
        time.sleep(120)  # Sleep for 2 minutes
