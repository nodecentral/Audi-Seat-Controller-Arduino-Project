// Main seat control sketch: reads all four switch-panel axes and drives the Cytron
// MDD10A driver(s) accordingly.
//
// Analog inputs use the Nano's own internal pull-up (INPUT_PULLUP), not an external 5V
// feed to the switch panel's PIN 6 — confirmed working this way, which resolves the
// earlier open question about what PIN 6 does: it isn't used at all.
//
// Threshold ranges (downMin/downMax, upMin/upMax) are confirmed working values for
// fore_aft and recline. front_tilt and rear_tilt aren't wired yet (see below) and use
// the same ranges as placeholders until measured with diagnostic_read_switch_panel.ino.
//
// Pin assignment: fore_aft ("seat base") and recline ("backrest") are the two axes
// currently built, on Cytron board #1 (M1/M2). front_tilt and rear_tilt are wired for a
// second Cytron board that hasn't been built yet — those two axes are inert until then.
// Confirmed: fore_aft on A3, recline on A5. front_tilt and rear_tilt share the remaining
// two analog pins (A1, A2) but which axis is on which is not yet confirmed — placeholder
// assignment below, correct it once that board is built and tested.
//
// Safety cutoff: if a direction is held continuously past MAX_RUN_MS, the motor is
// stopped regardless of switch state. This guards against a stuck button, broken wire,
// or mechanical jam holding a seat motor energized indefinitely.
//
// Power latch: the whole board (Nano, buck converter, both Cytron boards) sits behind an
// LCD-programmable delay-relay module (e.g. an XY-LJ02-style board) that handles wake and
// auto-off entirely on its own — no firmware involvement. A pushbutton wired into the
// module's own power-supply input (not just a trigger pin) wakes it; the module's relay
// then self-latches its own power on and drives a separate, properly-rated main relay that
// actually feeds the buck converter and Cytron board(s) (this module's own relay is only
// rated 5A, well under motor stall current, so it pilots the main relay rather than
// switching motor power itself). The module's own onboard timer (set generously, e.g.
// 10-15 minutes, directly on its LCD) cuts everything — including this Nano — after that
// period, regardless of what this sketch does. See README Power latch section for the full
// wiring and the current design's known open items.
//
// This sketch has no role in power management as a result: it can't accidentally keep the
// system powered (nothing here can prevent the module's timer from cutting power), and a
// hung/crashed Nano has no effect on the auto-off behavior either.

struct Axis {
  const char* name;
  uint8_t analogPin;
  uint8_t dirPin;
  uint8_t pwmPin;
  int downMin, downMax; // reading range that means "backward"
  int upMin, upMax;     // reading range that means "forward"
  int direction;        // currently commanded: -1, 0, 1
  unsigned long since;  // millis() when `direction` last changed
};

Axis axes[] = {
  { "fore_aft",    A3, 4, 5, 25, 30, 38, 43, 0, 0 }, // Cytron #1, M1 - confirmed working (seat base)
  { "recline",     A5, 7, 6, 25, 30, 38, 43, 0, 0 }, // Cytron #1, M2 - confirmed working (backrest)
  { "front_tilt",  A1, 2, 3, 25, 30, 38, 43, 0, 0 }, // Cytron #2 (not yet built), M1 - A1 vs A2 unconfirmed
  { "rear_tilt",   A2, 8, 9, 25, 30, 38, 43, 0, 0 }, // Cytron #2 (not yet built), M2 - A1 vs A2 unconfirmed
};

const unsigned long MAX_RUN_MS = 8000;
const uint8_t MOTOR_SPEED = 200; // 0-255 PWM duty cycle

void setup() {
  Serial.begin(115200);
  for (Axis& axis : axes) {
    pinMode(axis.dirPin, OUTPUT);
    pinMode(axis.pwmPin, OUTPUT);
    pinMode(axis.analogPin, INPUT_PULLUP);
  }
}

void loop() {
  unsigned long now = millis();

  for (Axis& axis : axes) {
    int reading = analogRead(axis.analogPin);
    int requested = 0;
    if (reading >= axis.downMin && reading <= axis.downMax) requested = -1;
    else if (reading >= axis.upMin && reading <= axis.upMax) requested = 1;

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
