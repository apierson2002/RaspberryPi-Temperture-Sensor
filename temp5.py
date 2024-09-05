# HEADER#########################################################################
# ANDREW PIERSON's TENNIS BALL SPEED REGRESSION MODEL
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
key = '###'
phone = #######
tempset= 41

# Load Modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sensor in the filesystem- source chat gpt
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave'

# read temp from device - source chat gpt
def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

# Read temp and return F* and C* - source chat gpt
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
        temp_f = round(temp_f,2)
        return temp_c, temp_f

# send text - source chat gpt
def send_text(phone, key, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone,
        'message': message,
        'key': key,
    })
    data = resp.json()
    return data
    
#control loop
quota =0
while True:
    temp_c, temp_f = read_temp()
    print(f'Temperature: {temp_c}°C, {temp_f}°F')
    time.sleep(2) #sleep for 2 sec
    if (temp_f>=tempset):
        tempstr = str(temp_f)
        text = 'Coach Bj, the walk-in is above 41*F.' + '\nTemp is: '+tempstr +'*F'
        data = send_text(phone, key, text)
        quota = data['quotaRemaining']
        count =0
        while (temp_f>=tempset):
            time.sleep(300) #5 min sleep
            count = count +1
            temp_c, temp_f = read_temp()
            print(f'Temperature: {temp_c}°C, {temp_f}°F')
            if (count==4):
                tempstr3 = str(temp_f)
                text3='It has been 20min and it is: ' + tempstr3 +'*F!' + '\n\nSomething could be wrong!!!'
                data = send_text(phone, key, text3)
        if (temp_f<=tempset):
            tempstr2 = str(temp_f)
            quotastr = str(quota)
            text2='The walk in is all Better now:) Temp: ' + tempstr2+'*F' +'\ntext-quota: '+quotastr
            data = send_text(phone, key, text2)
        time.sleep(120) #sleeps for 2 min



