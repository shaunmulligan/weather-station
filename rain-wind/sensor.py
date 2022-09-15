
#!/usr/bin/env python3
import sys
import errno
import os
import json
import time
import paho.mqtt.client as mqtt
import requests
import serial
import smbus2 as smbus

bus = smbus.SMBus(1)

def mqtt_detect():
    
    # Use the supervisor api to get services
    # See https://www.balena.io/docs/reference/supervisor/supervisor-api/
    
    address = os.getenv('BALENA_SUPERVISOR_ADDRESS', '')
    api_key = os.getenv('BALENA_SUPERVISOR_API_KEY', '')
    app_name = os.getenv('BALENA_APP_NAME', '')

    url = "{0}/v2/applications/state?apikey={1}".format(address, api_key)

    try:
        r = requests.get(url).json()
    except Exception as e:
        print("Error looking for MQTT service: {0}".format(str(e)))
        return False
    else:
        services = r[app_name]['services'].keys()

        if "mqtt" in services:
            return True
        else:
            return False

def weather(mclient, mqtt_addy):
    while True:
        ser = serial.Serial(
            port=os.environ.get('SERIAL_PORT', '/dev/ttyAMA0'),
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=10
        )
        
        # print("BME680 read to read? : ", bme_sensor.get_sensor_data())
        airdirections = []
        airspeed1s = []
        airspeed5s = []
        temperatures = []
        rainfall1hs = []
        rainfall24hs = []
        humiditys = []
        # barometrics = []
        done = False
        while not done:
            current_char = ser.read()
            # check for equals sign
            if current_char == b'c':
                airdirection = ser.read(4)
                airdirections.append(airdirection.decode('utf-8')[0:3])
                airspeed1 = ser.read(4)
                airspeed1s.append(airspeed1.decode('utf-8')[0:3])
                airspeed5 = ser.read(4)
                airspeed5s.append(airspeed5.decode('utf-8')[0:3])
                temperature = ser.read(4)
                temperatures.append(temperature.decode('utf-8')[0:3])
                rainfall1h = ser.read(4)
                rainfall1hs.append(rainfall1h.decode('utf-8')[0:3])
                rainfall24h = ser.read(4)
                rainfall24hs.append(rainfall24h.decode('utf8')[0:3])
                humidity = ser.read(2)
                humiditys.append(humidity.decode('utf-8')[0:2])
                # barometric = ser.read(6)
                # barometrics.append(barometric.decode('utf-8')[1:6])
            # this part will depend on your specific needs.
            # in this example, we stop after 10 readings
            # check for stopping condition and set done = True
            if len(airdirections) >= 1:
                done = True
        #
            for airdirection in range(len(airdirections)):
                airdirections[airdirection] = int(airdirections[airdirection])
        my_adval = ''.join(map(str, airdirections))
        #print("This is the values" + my_adval)
        my_int_ad = int(my_adval)
        my_ad = (my_int_ad)
        print ("Wind Direction:" + '%.2d' % my_ad + " Degrees")
        if my_ad  == 0:
            my_dir_ad = "North"
            print (my_dir_ad)
        elif my_ad == 45:
            my_dir_ad = "North East"
            print (my_dir_ad)
        elif my_ad == 90:
            my_dir_ad = "East"
            print (my_dir_ad)
        elif my_ad == 135:
            my_dir_ad = "South East"
            print (my_dir_ad)
        elif my_ad == 180:
            my_dir_ad = "South"
            print (my_dir_ad)
        elif my_ad == 225:
            my_dir_ad = "South West"
            print (my_dir_ad)
        elif my_ad == 270:
            my_dir_ad = "West"
            print (my_dir_ad)
        elif my_ad == 315:
            my_dir_ad = "North West"
            print (my_dir_ad)
        else:
            print ("Something else happened")

        ##
        ##AirSpeedAvg1###
        for airspeed1 in range(len(airspeed1s)):
            airspeed1s[airspeed1] = int(airspeed1s[airspeed1])
        my_as1val = ''.join(map(str, airspeed1s))
        #print("This is the AS1 value" + my_as1val)
        my_float_as1 = float(my_as1val)
        my_as1_initial = (my_float_as1 * 0.44704)
        print ("Average Wind Speed(1min):" + '%.2f' % my_as1_initial + "m/s")

        ###AirSpeedAvg2###
        for airspeed5 in range(len(airspeed5s)):
            airspeed5s[airspeed5] = int(airspeed5s[airspeed5])
        my_as5val = ''.join(map(str, airspeed5s))
        #print("This is the AS5 value" + my_as5val)
        my_float_as2 = float(my_as5val)
        my_as2_initial = (my_float_as2 * 0.44704)
        print ("Max Wind Speed(5min):" + '%.2f' % my_as2_initial + "m/s")

        ###Temperature####
        for temperature in range(len(temperatures)):
            temperatures[temperature] = int(temperatures[temperature])
        my_temperatureval = ''.join(map(str, temperatures))
        #print("This is the Temperature value" + my_temperatureval)
        my_float_temp = float(my_temperatureval)
        my_temp_initial = (my_float_temp - 32.00 )
        my_temp_5 = (my_temp_initial * 5.00 )
        my_temp_9 = (my_temp_5 / 9.00)
        print ("Temperature:" + '%.2f' % my_temp_9 + " Celcius")

        ###Rainfall 1H###
        for rainfall1h in range(len(rainfall1hs)):
            rainfall1hs[rainfall1h] = int(rainfall1hs[rainfall1h])
        my_rainfall1hval = ''.join(map(str, rainfall1hs))
        #print("This is the rainfall1h value" + my_rainfall1hval)
        my_float_rf1h = float(my_rainfall1hval)
        my_rf1h_initial = (my_float_rf1h * 25.40)
        my_rf1h_next = (my_rf1h_initial * 0.01)
        print ("Rainfall(1hr):" + '%.2f' % my_rf1h_next + "mm")

        ###Rainfall 24H###
        for rainfall24h in range(len(rainfall24hs)):
            rainfall24hs[rainfall24h] = int(rainfall24hs[rainfall24h])
        my_rainfall24hval = ''.join(map(str, rainfall24hs))
        #print("This is the rainfall24h value" + my_rainfall24hval)
        my_float_rf24h = float(my_rainfall24hval)
        my_rf24h_initial = (my_float_rf24h * 25.40)
        my_rf24h_next = (my_rf24h_initial * 0.01)
        print ("Rainfall(24hr):" + '%.2f' % my_rf24h_next + "mm")

        ###Humidity###
        for humidity in range(len(humiditys)):
            humiditys[humidity] = int(humiditys[humidity])
        my_humidityval = ''.join(map(str, humiditys))
        my_int_humidity = int(my_humidityval)
        my_humidity = (my_int_humidity)
        print ("Humidity:" + '%.2d' % my_humidity + "%")

        # ###Barometric Pressure###
        # for barometric in range(len(barometrics)):
        #     barometrics[barometric] = int(barometrics[barometric])
        # my_barometricval = ''.join(map(str, barometrics))
        # #print("value of barometer:" + my_barometricval)
        # my_float_barometric = float(my_barometricval)
        # my_barometric_total = (my_float_barometric / 10.00)
        # print ("Barometric Pressure:" + '%.2f' % my_barometric_total + "hPa")

        sensor_data = {
            "Wind_Direction" : my_dir_ad,
            "Average Wind Speed(1min)" : my_as1_initial,
            "Max Wind Speed(5min)" : my_as2_initial,
            "Box Temperature" : my_temp_9,
            "Rainfall(1hr)" : my_rf1h_next,
            "Rainfall(24hr)" : my_rf24h_next,
            "Box Humidity" : my_humidity,
        }
        mclient.publish('sensors', json.dumps(sensor_data))
        # r = requests.post('http://connector:8080', json=sensor_data)
        time.sleep( 2 )

if __name__ == "__main__":
    mqtt_address = os.getenv('MQTT_ADDRESS', 'none')
    publish_interval = os.getenv('MQTT_PUB_INTERVAL', '8')

    try:
        interval = float(publish_interval)
    except Exception as e:
        print("Error converting MQTT_PUB_INTERVAL: Must be integer or float! Using default.")
        interval = 8

    if mqtt_detect() and mqtt_address == "none":
        mqtt_address = "mqtt"

    if mqtt_address != "none":
        print("Starting mqtt client, publishing to {0}:1883".format(mqtt_address))
        print("Using MQTT publish interval: {0} sec(s)".format(interval))
        client = mqtt.Client()
        try:
            client.connect(mqtt_address, 1883, 60)
        except Exception as e:
            print("Error connecting to mqtt. ({0})".format(str(e)))
            mqtt_address = "none"

        weather(client, mqtt_address)