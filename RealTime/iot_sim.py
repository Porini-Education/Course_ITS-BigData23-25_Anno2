# A simple Python script that simulates an IoT device sending temperature, wind, and humidity data. 
# This script uses the random library to generate random sensor data and time library to pause the script for a certain amount of time between sending data.
# It will print out the sensor readings every 2 seconds. 
# You can replace the print statement with code to send the data to a server or save it to a file.
# Please note that this is a very basic example and a real-world IoT device would be more complex and would need to handle errors and other edge cases.

import json
import random
import time
import psutil

class Sensor:
    def __init__(self, name, initialValue, min_value=None, max_value=None):
        self.name = name
        self.lastValue = initialValue
        self.min_value = min_value
        self.max_value = max_value

    def read_data(self):
        self.lastValue += random.uniform(-5.0, 5.0)
        if self.max_value is not None:
            self.lastValue = min(self.max_value, self.lastValue)
        if self.min_value is not None:
            self.lastValue = max(self.min_value, self.lastValue)
        return round(self.lastValue, 2)

class IoTDevice:
    def __init__(self, sensors):
        self.sensors = sensors

    def get_json_data(self):
        data = {sensor.name: sensor.read_data() for sensor in self.sensors}
        return json.dumps(data)
    
class DataSender:
    def __init__(self, device:IoTDevice) -> None:
        self.device = device
    
    def send_data(self):
        # Code to send data to a server or save it to a file
        print(self.device.get_json_data())

def main():
    # Create sensors
    temp_sensor = Sensor("Temperature", 20, -10, 40)
    wind_sensor = Sensor("Wind", 1, 0, 100)
    humidity_sensor = Sensor("Humidity", 30, 0, 100)

    # Create IoT device with sensors
    device = IoTDevice([temp_sensor, wind_sensor, humidity_sensor])

    sender = DataSender(device)
    # Send data every 2 seconds
    while True:
        sender.send_data()
        time.sleep(2)

if __name__ == "__main__":
    main()