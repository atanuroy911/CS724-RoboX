int enA = 2;
int in1 = 3;
int in2 = 4;
int enB = 7;
int in3 = 5;
int in4 = 6;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);

  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  analogWrite(enA, 255);
  analogWrite(enB, 255);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    // Check for valid commands, ignoring newline characters
    if (cmd != '\n') {
      Serial.print("Command received: ");
      Serial.println(cmd);
      cmd = toupper(cmd);

      // Control motors using WASD commands
      switch (cmd) {
        case 'W':
          // Move forward
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH);
          digitalWrite(in3, LOW);
          digitalWrite(in4, HIGH);
          break;
        case 'S':
          // Move backward
          digitalWrite(in1, HIGH);
          digitalWrite(in2, LOW);
          digitalWrite(in3, HIGH);
          digitalWrite(in4, LOW);
          break;
        case 'D':
          // Turn right
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH);
          digitalWrite(in3, LOW);
          digitalWrite(in4, LOW);
          break;
        case 'A':
          // Turn left
          digitalWrite(in1, LOW);
          digitalWrite(in2, LOW);
          digitalWrite(in3, LOW);
          digitalWrite(in4, HIGH);
          break;
        case 'X':
          // Stop
          digitalWrite(in1, LOW);
          digitalWrite(in2, LOW);
          digitalWrite(in3, LOW);
          digitalWrite(in4, LOW);
          break;
        default:
          // Invalid command
          Serial.println("Invalid command.");
      }
    }
  }
}
