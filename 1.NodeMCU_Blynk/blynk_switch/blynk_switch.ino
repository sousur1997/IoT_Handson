#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#define BLYNK_TEMPLATE_ID "**********"
#define BLYNK_TEMPLATE_NAME "**********"
#define BLYNK_AUTH_TOKEN "**********"

const char* auth = BLYNK_AUTH_TOKEN;
const char* ssid = "AndroidAP";     // Replace with your WiFi network SSID
const char* password = "ssur1997"; // Replace with your WiFi network password

const int ledPin = D0; // GPIO 16 (D0) for the LED
const int cloud_switch_led_pin = D1;

BlynkTimer timer;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT); // Set the LED pin as an OUTPUT
  pinMode(cloud_switch_led_pin, OUTPUT); // Set the LED pin as an OUTPUT

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

  delay(10);
  Blynk.begin(auth, ssid, password);
}

BLYNK_WRITE(V0)
{
  // Set incoming value from pin V0 to a variable
  int value = param.asInt();
  if(value == 1){
    digitalWrite(cloud_switch_led_pin, HIGH);
  }else{
    digitalWrite(cloud_switch_led_pin, LOW);
  } 
} 

void loop() {
  // put your main code here, to run repeatedly:
  Blynk.run();
}
