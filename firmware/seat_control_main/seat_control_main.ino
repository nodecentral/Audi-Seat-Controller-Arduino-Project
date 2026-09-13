// Main seat control sketch: reads all four switch-panel axes and drives the Cytron
// MDD10A driver(s) accordingly.
//
// Threshold values (downMax/upMax) are copied from the confirmed PIN 1 (front_tilt)
// measurement in README.md (idle ~1023, down ~27-28, up ~40-41). The other three axes
// use the same placeholder thresholds until measured independently with
// diagnostic_read_switch_panel.ino — narrow or widen them once real numbers are in.
//
// Pin assignment: front_tilt and fore_aft go to Cytron board #1 (M1/M2). rear_tilt and
// recline are wired for a second Cytron board that hasn't been built yet (see README
// Next Steps) — those two axes are inert until that board exists.
//
// Safety cutoff: if a direction is held continuously past MAX_RUN_MS, the motor is
// stopped regardless of switch state. This guards against a stuck button, broken wire,
// or mechanical jam holding a seat motor energized indefinitely.

struct Axis {
  const char* name;
  uint8_t analogPin;
  uint8_t dirPin;
  uint8_t pwmPin;
  int downMax;
  int upMax;
  int direction;       // currently commanded: -1, 0, 1
  unsigned long since; // millis() when `direction` last changed
};

Axis axes[] = {
  { "front_tilt", A0, 2, 3, 35, 50, 0, 0 }, // Cytron #1, M1
  { "fore_aft",   A2, 7, 6, 35, 50, 0, 0 }, // Cytron #1, M2
  { "rear_tilt",  A1, 4, 5, 35, 50, 0, 0 }, // Cytron #2 (not yet built), M1
  { "recline",    A3, 8, 9, 35, 50, 0, 0 }, // Cytron #2 (not yet built), M2
};

const unsigned long MAX_RUN_MS = 8000;
const uint8_t MOTOR_SPEED = 200; // 0-255 PWM duty cycle

void setup() {
  Serial.begin(115200);
  for (Axis& axis : axes) {
    pinMode(axis.dirPin, OUTPUT);
    pinMode(axis.pwmPin, OUTPUT);
  }
}

void loop() {
  unsigned long now = millis();

  for (Axis& axis : axes) {
    int reading = analogRead(axis.analogPin);
    int requested = 0;
    if (reading <= axis.downMax) requested = -1;
    else if (reading <= axis.upMax) requested = 1;

    if (requested != axis.direction) {
      axis.direction = requested;
      axis.since = now;
    } else if (requested != 0 && now - axis.since > MAX_RUN_MS) {
      requested = 0; // safety cutoff
    }

    digitalWrite(axis.dirPin, requested > 0 ? HIGH : LOW);
    analogWrite(axis.pwmPin, requested == 0 ? 0 : MOTOR_SPEED);
  }
}
