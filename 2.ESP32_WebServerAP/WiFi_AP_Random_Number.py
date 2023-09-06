import network
import socket
import urandom
import time

# Create an access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32-AP')  # Set the AP SSID (Wi-Fi name)
ap.config(authmode=network.AUTH_OPEN)  # No password (open network)

# HTML template
html = """<!DOCTYPE html>
<html>
<head><title>Random Number</title></head>
<body>
<h1>Random Number: <span id="random"></span></h1>
<script>
function updateRandom() {
    fetch('/random')
        .then(response => response.text())
        .then(data => {
            document.getElementById('random').textContent = data;
            updateRandom();  // Continuously fetch and update the random number
        });
}
updateRandom();  // Start updating the random number
</script>
</body>
</html>
"""

# Create a socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.4.1', 80))  # Set the ESP32's default IP address
s.listen(1)  # Listen for a single connection

print("Access Point created with SSID 'ESP32-AP'.")
print("Connect to 'ESP32-AP' and open http://192.168.4.1/ in your web browser to see the random numbers.")

while True:
    conn, addr = s.accept()
    print("Connected to %s" % str(addr))

    request = conn.recv(1024)
    if not request:
        break

    conn.sendall('HTTP/1.1 200 OK\n')
    conn.sendall('Content-Type: text/html\n')
    conn.sendall('Connection: close\n\n')

    if '/random' in request.decode('utf-8'):
        # Generate and send a random number
        random_number = urandom.getrandbits(16)
        conn.sendall(str(random_number))

    else:
        # Serve the HTML page
        conn.sendall(html)

    conn.close()

