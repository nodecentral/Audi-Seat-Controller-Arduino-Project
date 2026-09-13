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
//
// Power latch: the whole board (Nano, buck converter, both Cytron boards) sits behind a
// retriggerable delay-off relay module (e.g. an SRD-12VDC-SL-C based "trigger delay turn
// off" board) on the permanent 12V feed, normally off. A momentary pushbutton wired to the
// module's trigger input wakes it; the module's own onboard timer (its potentiometer,
// independent of this sketch) then holds the relay closed for a short window (set toward
// the top of its range, e.g. 5-10s) before cutting power on its own.
//
// POWER_KEEPALIVE_PIN mimics the pushbutton — via a small transistor wired in parallel with
// it, not driven directly into the trigger input — pulsing periodically as long as there's
// genuine switch-panel activity, which retriggers the module's timer and keeps the system
// awake for as long as the seat is actually being adjusted. Once STANDBY_TIMEOUT_MS passes
// with no activity, this sketch simply stops pulsing; the module's own short timer expires
// shortly after and cuts all power, including to this Nano.
//
// This split matters: because the final cutoff is done by the module's own hardware timer
// rather than this sketch holding a pin high indefinitely, a hung or crashed Nano can't keep
// the system powered forever — it can only fail to extend the (short) delay, which is a much
// safer failure mode for something sitting on a permanent 12V feed.
//
// Unverified: that the module's trigger input is actually retriggerable (repeated triggers
// reset/extend the countdown rather than being ignored) — confirm on the bench before
// wiring this in. See README Power latch section.

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

const uint8_t POWER_KEEPALIVE_PIN = 12;
const unsigned long STANDBY_TIMEOUT_MS = 5UL * 60UL * 1000UL;  // give up after 5 min idle
const unsigned long KEEPALIVE_INTERVAL_MS = 2000;              // must stay well under the
                                                                // module's own delay setting
const unsigned long KEEPALIVE_PULSE_MS = 100;
unsigned long lastActivityMs = 0;
unsigned long lastKeepaliveMs = 0;
bool keepaliveHigh = false;

void setup() {
  Serial.begin(115200);
  for (Axis& axis : axes) {
    pinMode(axis.dirPin, OUTPUT);
    pinMode(axis.pwmPin, OUTPUT);
  }
  pinMode(POWER_KEEPALIVE_PIN, OUTPUT);
  digitalWrite(POWER_KEEPALIVE_PIN, LOW);
  lastActivityMs = millis();
}

void loop() {
  unsigned long now = millis();
  bool anyActivity = false;

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

    if (requested != 0) anyActivity = true;

    digitalWrite(axis.dirPin, requested > 0 ? HIGH : LOW);
    analogWrite(axis.pwmPin, requested == 0 ? 0 : MOTOR_SPEED);
  }

  if (anyActivity) {
    lastActivityMs = now;
  }

  bool awake = (now - lastActivityMs) < STANDBY_TIMEOUT_MS;
  if (awake) {
    // Pulse periodically to retrigger the delay-off module, mimicking a fresh button press.
    if (!keepaliveHigh && now - lastKeepaliveMs >= KEEPALIVE_INTERVAL_MS) {
      digitalWrite(POWER_KEEPALIVE_PIN, HIGH);
      keepaliveHigh = true;
      lastKeepaliveMs = now;
    } else if (keepaliveHigh && now - lastKeepaliveMs >= KEEPALIVE_PULSE_MS) {
      digitalWrite(POWER_KEEPALIVE_PIN, LOW);
      keepaliveHigh = false;
    }
  }
  // else: stop pulsing and let the module's own timer expire and cut power.
}
