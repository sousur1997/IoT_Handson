import machine
import network
import socket

# define the pin number for the built-in LED on the ESP32
led_pin = 2

# create a Pin object for the LED pin
led = machine.Pin(led_pin, machine.Pin.OUT)

# create a WiFi access point with the given SSID and password
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='MyESP32AP', password='mypassword')

# define the HTML content for the web page
html = """<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ESP32 LED Control</title>
    <style>
      body { font-family: Arial, Helvetica, sans-serif; }
      .container { display: flex; flex-direction: column; align-items: center; }
      .led { margin-top: 30px; width: 100px; height: 100px; border-radius: 50%; background-color: #CCCCCC; }
      .button { margin-top: 20px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>ESP32 LED Control</h1>
      <div class="led" id="led"></div>
      <button class="button" onclick="toggleLed()">Toggle LED</button>
    </div>
    <script>
		var isOn = false;
      function toggleLed() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/toggle');
        xhr.send();
		
		isOn = !isOn;
        document.getElementById('led').classList.toggle('on');
		if(isOn){
			document.getElementById('led').style.backgroundColor = "#4284df";
		}else{
			document.getElementById('led').style.backgroundColor = "#CCCCCC";
		}
		
      }
    </script>
  </body>
</html>"""

# create a function to handle incoming client requests
def handle_request(conn):
    request = conn.recv(1024)
    method, path, version = request.decode().split('\r\n')[0].split()
    if path == '/':
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)
    elif path == '/toggle':
        led.value(not led.value())
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK')
    conn.close()

# create a socket and bind it to the IP address and port number of the access point
s = socket.socket()
s.bind((ap.ifconfig()[0], 80))
s.listen(5)

# loop forever, handling incoming client requests
while True:
    conn, addr = s.accept()
    handle_request(conn)


