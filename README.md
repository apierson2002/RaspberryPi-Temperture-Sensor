### RaspberryPi-Temperture-Sensor for The Shoals Shack ###

I was tasked to replace the broken temperature sensor device for my managers walk-in cooler at my college summer job, www.theshoalsshack.com. 

This python script uses the glob library to take the temperature with a connected sensor to the Raspberry Pi. The Request 
library and www.textbelt.com API were used to send a text to my boss when the cooler reaches a certain temperature.

To make the program work practically, I have the Raspberry Pi set up to run the script automatically as a startup service.
