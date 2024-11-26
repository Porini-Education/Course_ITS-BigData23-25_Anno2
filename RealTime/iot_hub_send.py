# A simple Python script that simulates an IoT device sending temperature, wind, and humidity data.
# Please note that this is a very basic example and a real-world IoT device would be more complex and would need to handle errors and other edge cases.

import json
import os
import time
import psutil
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

class Sensor:
    def __init__(self, name, call, values=None):
        self.name = name
        self.call = call
        self.values = values

    def read_data(self):
        if self.values is not None:
            return {value: getattr(self.call(), value) for value in self.values}
        return self.call()

class IoTDevice:
    def __init__(self, sensors, flatten_data=False):
        self.sensors = sensors
        self.flatten_data = flatten_data

    def get_json_data(self):
        data = {sensor.name: sensor.read_data() for sensor in self.sensors}

        if self.flatten_data:
            #flatten the data dictionary, not all the sensors return a dictionary
            for key in list(data.keys()):
                if not isinstance(data[key], dict):
                    data[key] = {key: data[key]}
                else:
                    data[key] = {f"{key}_{k}": v for k, v in data[key].items()}

            data = {k: v for sensor_data in data.values() for k, v in sensor_data.items()}

        data["timestamp"] = datetime.datetime.timestamp(datetime.datetime.now())
        return json.dumps(data)
    
class IotHubSender:
    CONNECTION_STRING = "HostName=iot-hub-wru.azure-devices.net;DeviceId=PythonApp1;SharedAccessKey=GwwOtBACa0/MGtXcj+5Aml29bcMJ29wFKiZi9DLKeto=" # Add your connection string here
    def __init__(self, device:IoTDevice) -> None:
        self.device = device
        self.client = IoTHubDeviceClient.create_from_connection_string(self.CONNECTION_STRING)
    
    def send_data(self):
        message = Message(self.device.get_json_data())
        self.client.send_message(message)
        print("Message sent to Azure IoT Hub")

def main():
    # Create sensors
    cpu_perc_sensor = Sensor("CPU %", psutil.cpu_percent)
    cpu_freq_sensor = Sensor("CPU Freq", psutil.cpu_freq, ["current", "min", "max"])
    memory_sensor = Sensor("Memory", psutil.virtual_memory, ["total", "available", "percent", "used", "free"])

    # Create IoT device with sensors
    device = IoTDevice([cpu_perc_sensor, cpu_freq_sensor, memory_sensor], flatten_data=True)

    sender = IotHubSender(device)
    # Send data every 2 seconds
    while True:
        sender.send_data()
        time.sleep(2)

if __name__ == "__main__":
    main()