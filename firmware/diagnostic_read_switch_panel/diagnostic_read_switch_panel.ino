// Reads the four candidate movement lines from the Preh switch panel and prints raw
// 10-bit ADC values over serial (115200 baud).
//
// Use this to fill in the still-missing rows of the ADC table in README.md: hold each
// direction button on each axis and record the steady-state reading. PIN 1 (front tilt)
// is already confirmed: idle ~1023, down ~27-28, up ~40-41 — the other three axes are
// expected to follow the same pattern but haven't been measured yet.
//
// Also wire PIN 6 to 5V for this test (per the pull-up hypothesis in README.md) and watch
// whether the idle reading drops from ~1023 to something else if PIN 6 is left floating —
// that's the quickest way to sanity-check the hypothesis before committing to it in wiring.

const int PIN_FRONT_TILT = A0; // switch PIN 1
const int PIN_REAR_TILT  = A1; // switch PIN 2
const int PIN_FORE_AFT   = A2; // switch PIN 3
const int PIN_RECLINE    = A3; // switch PIN 5

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print("front_tilt=");
  Serial.print(analogRead(PIN_FRONT_TILT));
  Serial.print("  rear_tilt=");
  Serial.print(analogRead(PIN_REAR_TILT));
  Serial.print("  fore_aft=");
  Serial.print(analogRead(PIN_FORE_AFT));
  Serial.print("  recline=");
  Serial.println(analogRead(PIN_RECLINE));
  delay(200);
}
