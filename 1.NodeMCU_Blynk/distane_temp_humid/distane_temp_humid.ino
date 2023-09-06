#define TRIGGER_PIN  D5 
#define ECHO_PIN     D6 
#define MAX_DISTANCE 400 // Maximum distance we want to measure (in centimeters)

#define DHT_PIN      D2 // GPIO 4
#define DHT_TYPE     DHT11 // DHT11 sensor

#include <DHT.h>

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dht.begin();
}

void loop() {
  // Measure distance with the HC-SR04 ultrasonic sensor
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

  delay(5000); // Wait for 5 seconds before the next reading
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
