#include <ESP8266WiFi.h>

const char* ssid = "AndroidAP";     // Replace with your WiFi network SSID
const char* password = "ssur1997"; // Replace with your WiFi network password
const int ledPin = D0; // GPIO 16 (D0) for the LED

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT); // Set the LED pin as an OUTPUT

  // Connect to WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(ledPin, LOW); // Turn off the LED while attempting to connect
    delay(500);
    Serial.print(".");
  }

  digitalWrite(ledPin, HIGH); // Turn on the LED when WiFi is connected

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Your code here (if any)
}
