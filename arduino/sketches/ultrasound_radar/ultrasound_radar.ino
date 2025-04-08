#include <Servo.h>

Servo myServo;
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  Serial.begin(9600);
  myServo.attach(6);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  for (int angle = 2; angle <= 178; angle++) {
    myServo.write(angle);
    delay(15); // Let servo move

    // Trigger ultrasonic sensor
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2; // Convert to cm

    // Send data to serial in format: angle,distance
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);

    delay(30); // Adjust for smoother data
  }

  // Sweep back
  for (int angle = 178; angle >= 2; angle--) {
    myServo.write(angle);
    delay(15);

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);

    delay(30);
  }
}
