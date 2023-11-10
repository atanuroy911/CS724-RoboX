#include <SoftwareSerial.h>

SoftwareSerial bluetooth(0, 1); // RX, TX pins on Arduino

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);  // Default baud rate for HC-05
}

void loop() {
  if (bluetooth.available()) {
    char receivedChar = bluetooth.read();
    Serial.print("Received: ");
    Serial.println(receivedChar);
  }

  if (Serial.available()) {
    char sendChar = Serial.read();
    bluetooth.write(sendChar);
  }
}
