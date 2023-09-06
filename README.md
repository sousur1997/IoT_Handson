# IoT Hands-on Training

This hands-on training will cover basic WiFi and Bluetooth connectivity with ESP8266, ESP32, and Seeed Studio XIAO BLE Sense.

## ESP8266

The [ESP8266](https://www.espressif.com/en/products/socs/esp8266) is a popular low-cost WiFi microcontroller by Espressif. We will use it to connect to WiFi and send sensor data.

### 1. Basic WiFi Setup

- Use the [Arduino IDE](https://www.arduino.cc/en/software) to program the ESP8266  
- Include the [ESP8266WiFi library](https://github.com/esp8266/Arduino/tree/master/libraries/ESP8266WiFi)
- Call `WiFi.begin(ssid, password)` to connect to the WiFi access point
- Light an LED when successfully connected using `digitalWrite`

### 2. Distance and Temperature Sensor  

- Use an [HC-SR04 ultrasonic sensor](https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/) to measure distance
- Use a [DHT11 temperature sensor](https://learn.adafruit.com/dht/overview) to read temperature
- Output readings to [Arduino serial monitor]

### 3. Blynk IoT Platform

- Create a [Blynk](https://blynk.io/) account and auth token
- Install the [Blynk library](https://github.com/blynkkk/blynk-library)
- Create a button widget to control the LED  
- Output distance and temperature values to virtual pins

### 4. Visualize Sensor Data  

- Build a dashboard in the Blynk app
- Add graph widgets to display distance and temperature plots
- Stream data from the ESP8266 to update the dashboard  

## ESP32

The [ESP32](https://www.espressif.com/en/products/socs/esp32) is a more powerful WiFi + Bluetooth chip. We will create a simple web server.

### 1. Simple Web Server

- Set the ESP32 into [Soft AP mode]
- Serve a simple web page with a button  
- Use JavaScript to toggle the onboard LED

### 2. Display Random Data

- Generate random numbers in C++ on the ESP32
- Serve them on the web page with JavaScript 
- Refresh to get new values

## Seeed Studio XIAO BLE Sense  

The [XIAO BLE Sense](https://wiki.seeedstudio.com/XIAO_BLE/) is a Seeed Studio board with built-in BLE and sensors.

### 1. BLE Temperature Sensor

- Read the internal temperature sensor
- Create a BLE service and characteristic
- Send temperature values over BLE 
- View data in the serial monitor

### 2. BLE Messaging

- Add a read/write string characteristic
- Send messages from an app like [nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-mobile)
- Print received messages to the serial monitor 
