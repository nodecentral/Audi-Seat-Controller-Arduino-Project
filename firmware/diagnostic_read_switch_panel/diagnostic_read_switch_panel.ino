// Reads the four movement lines from the Preh switch panel and prints raw 10-bit ADC
// values over serial (115200 baud).
//
// Uses the Nano's internal pull-up (INPUT_PULLUP) — confirmed working this way, switch
// panel PIN 6 is not used at all.
//
// fore_aft (A3) and recline (A5) are confirmed working: idle ~1023, backward ~25-30,
// forward ~38-43. front_tilt and rear_tilt share A1/A2 but which is which isn't confirmed
// yet (that board isn't built) — use this sketch to find out once it is: hold each
// direction button and record the steady-state reading here.

const int PIN_FORE_AFT   = A3; // confirmed - "seat base"
const int PIN_RECLINE    = A5; // confirmed - "backrest"
const int PIN_AXIS_A1    = A1; // front_tilt or rear_tilt - not yet confirmed which
const int PIN_AXIS_A2    = A2; // front_tilt or rear_tilt - not yet confirmed which

void setup() {
  Serial.begin(115200);
  pinMode(PIN_FORE_AFT, INPUT_PULLUP);
  pinMode(PIN_RECLINE, INPUT_PULLUP);
  pinMode(PIN_AXIS_A1, INPUT_PULLUP);
  pinMode(PIN_AXIS_A2, INPUT_PULLUP);
}

void loop() {
  Serial.print("fore_aft=");
  Serial.print(analogRead(PIN_FORE_AFT));
  Serial.print("  recline=");
  Serial.print(analogRead(PIN_RECLINE));
  Serial.print("  A1=");
  Serial.print(analogRead(PIN_AXIS_A1));
  Serial.print("  A2=");
  Serial.println(analogRead(PIN_AXIS_A2));
  delay(200);
}
