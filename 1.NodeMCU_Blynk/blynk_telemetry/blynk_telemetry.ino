#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <DHT.h>

#define BLYNK_TEMPLATE_ID "**********"
#define BLYNK_TEMPLATE_NAME "**********"
#define BLYNK_AUTH_TOKEN "**********"

#define TRIGGER_PIN  D5 
#define ECHO_PIN     D6 
#define MAX_DISTANCE 400 // Maximum distance we want to measure (in centimeters)

#define DHT_PIN      D2 // GPIO 4
#define DHT_TYPE     DHT11 // DHT11 sensor

const char* auth = BLYNK_AUTH_TOKEN;
const char* ssid = "AndroidAP";     // Replace with your WiFi network SSID
const char* password = "ssur1997"; // Replace with your WiFi network password

const int ledPin = D0; // GPIO 16 (D0) for the LED
const int cloud_switch_led_pin = D1;

DHT dht(DHT_PIN, DHT_TYPE);
BlynkTimer timer;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht.begin();
  
  pinMode(ledPin, OUTPUT); // Set the LED pin as an OUTPUT
  pinMode(cloud_switch_led_pin, OUTPUT); // Set the LED pin as an OUTPUT

  pinMode(ECHO_PIN, INPUT);   // set Echo pin as Input
  pinMode(TRIGGER_PIN, OUTPUT);  // set Trig pin as Output

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
  float distance = measureDistance();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Read temperature and humidity with the DHT11 sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (!isnan(humidity) && !isnan(temperature)) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C\t");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
    Serial.println("Failed to read from DHT sensor.");
  }

  Blynk.virtualWrite(V1, temperature);
  Blynk.virtualWrite(V2, humidity);
  Blynk.virtualWrite(V3, distance);

  delay(100); // Wait for 100 ms before the next reading
}

float measureDistance() {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  // Calculate distance in centimeters (cm)
  float distance = (float)(duration * 0.0343 / 2);

  return distance;
}
