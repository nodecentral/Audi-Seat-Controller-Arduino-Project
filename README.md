Audi Q8 (2022) S-Line Electric Seat — 4N095747D Control Switch

Reverse-Engineering & Arduino Standalone Controller — Working Notes

1. Objective

The original Audi seat control electronics/module is missing.

The objective is to retain the original Audi seat adjustment controls and use them as a standalone control interface for the 12V electric seat motors in a different vehicle.

The proposed architecture is:

Audi 4N095747D switch assembly
          ↓
Arduino — reads/decode switch signals
          ↓
High-current H-bridge motor drivers
          ↓
12V seat motors

The Audi switch assembly is NOT being used to supply motor current. It is only being used as a low-current control input.

⸻

2. 4N095747D Switch PCB — Findings

The 4N095747D is the seat adjustment switch/control assembly.

The PCB was physically inspected.

Important observations:

* The PCB contains the physical seat adjustment controls.
* No obvious microcontroller was found.
* No CAN/LIN transceiver was found.
* No high-current motor-driving components were found.
* The PCB therefore appears to be a passive control/signal interface rather than the seat motor controller.
* The connector has 12 positions physically, but only the TOP ROW of 6 pins is currently relevant/used.
* The bottom row has not been identified as being used for the functions under investigation.
* There are resistors on the PCB, consistent with the control signals being encoded electrically rather than simply providing a separate wire for every direction.

⸻

3. Connector Pin Arrangement

Viewed as previously identified:

TOP ROW
PIN 1   PIN 2   PIN 3   PIN 4   PIN 5   PIN 6

Only these six top-row positions are currently being used.

PIN 4 has been identified as the COMMON connection.

For testing, Pin 4 has been connected to Arduino GND.

⸻

4. Confirmed Functional Pin Mapping

The following has been established by continuity testing of the switch assembly.

Pin	Function
PIN 1	Front of seat base tilt — UP / DOWN
PIN 2	Rear of seat base tilt — UP / DOWN
PIN 3	Entire seat — FORWARD / BACKWARD
PIN 4	COMMON / reference / GND
PIN 5	Seat backrest — FORWARD / BACKWARD (recline)
PIN 6	Not yet assigned / not currently required

Therefore:

PIN 1 ↔ PIN 4 = front seat-base tilt control
PIN 2 ↔ PIN 4 = rear seat-base tilt control
PIN 3 ↔ PIN 4 = complete seat forward/back movement
PIN 5 ↔ PIN 4 = backrest recline movement

PIN 4 is common to the control functions.

⸻

5. Important Discovery About Direction

Continuity testing showed an important characteristic:

Moving a control in either direction produces continuity between the relevant control pin and Pin 4.

For example:

PIN 1 + PIN 4

produces a circuit/continuity when the front-seat tilt control is moved in either direction.

Therefore the direction is NOT determined simply by:

Direction A = different pair of pins
Direction B = another pair of pins

Instead, the electrical characteristics of the circuit change depending on which direction the control is moved.

This strongly indicates that the resistors on the PCB are being used to encode the direction.

⸻

6. Arduino Test — First Confirmed Measurement

An Arduino was connected to the switch assembly to investigate the electrical signal.

Initial test:

Seat PIN 4 → Arduino GND
Seat PIN 1 → Arduino A0

The Arduino was connected to the PC by USB.

The Arduino was configured to read the analogue input.

With the control in its neutral/unpressed state:

PIN 1 / A0 = approximately 1023

This indicates that the input is effectively at the top of the Arduino ADC range when no adjustment is being requested.

⸻

7. Confirmed PIN 1 Measurements

The front seat-base tilt control was then tested in both directions.

Front seat tilt DOWN

Arduino reading:

approximately 27–28

The reading fluctuated slightly between 27 and 28.

Front seat tilt UP

Arduino reading:

approximately 40–41

Again, the reading fluctuated slightly, approximately 40–41.

PIN 1 results

Control state	Arduino ADC reading
Neutral / nothing pressed	~1023
Front seat tilt DOWN	~27–28
Front seat tilt UP	~40–41

These are VERY strong evidence that the two directions are electrically distinguishable.

The small fluctuations are not considered significant. They can be caused by normal ADC noise, switch/contact pressure, resistor tolerance, USB power variation, etc.

The software should therefore use ranges rather than relying on one exact ADC number.

⸻

8. Current Electrical Interpretation

The working hypothesis is now:

PIN 4 = common/reference

Each control pin is associated with a particular seat function.

The physical rocker/switch changes the resistance network when moved in one direction or the other.

Conceptually:

PIN X
   │
   ├── resistance network
   │
switch mechanism
   │
PIN 4 / COMMON

The Arduino measures the resulting analogue voltage.

The exact resistor values and voltage-divider arrangement have NOT yet been fully mapped.

Therefore, we should describe this as:

"analogue/resistance encoded switch outputs"

rather than claiming we have completely reverse-engineered the original Audi circuit.

⸻

9. Why the Arduino Approach Is Being Used

The Arduino provides a convenient way of measuring the analogue signal produced by the original Audi control.

Instead of trying to reproduce the missing Audi seat ECU, we can make our own controller.

The Arduino will eventually perform two jobs:

1. Decode the Audi switch signals.
2. Control the motor-driver hardware.

The switch PCB itself remains a low-current input device.

The Arduino does NOT drive the seat motors directly.

⸻

10. Proposed Arduino Control Architecture

┌──────────────────────────────┐
│ Audi 4N095747D Switch PCB    │
│                              │
│ Pin 1 ───── analogue input   │
│ Pin 2 ───── analogue input   │
│ Pin 3 ───── analogue input   │
│ Pin 4 ───── Arduino GND      │
│ Pin 5 ───── analogue input   │
│ Pin 6 ───── TBD              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Arduino                      │
│                              │
│ Read analogue values         │
│ Identify direction           │
│ Apply thresholds/ranges      │
│ Generate motor commands      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ High-current H-bridge        │
│ motor drivers                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 12V Seat Motors              │
│                              │
│ Forward / Reverse            │
└──────────────────────────────┘

⸻

11. Important Principle for the Final Motor System

The Arduino will only provide LOW-CURRENT control signals.

The seat motors will have their own 12V/high-current power supply.

A motor requires polarity reversal to change direction:

+12V / 0V  → Motor direction A
0V / +12V  → Motor direction B

Therefore each motor requires a suitable H-bridge or equivalent reversing arrangement.

The previously discussed approach is to use high-current H-bridge motor drivers rather than attempting to switch the motors directly from the Arduino.

⸻

12. What Has NOT Yet Been Established

The following should remain marked as TBD:

* Exact resistance values used by each switch direction.
* Exact analogue voltage corresponding to every control position.
* PIN 6 function.
* Whether PIN 6 is required for another seat function or is unused.
* Exact number of motors in the particular seat.
* Which motor corresponds to each physical adjustment.
* Motor current requirements, particularly stall current.
* Whether the seat motors contain any additional position/safety circuitry.
* Whether any seat functions require additional feedback signals.
* Final motor-driver choice.
* Final Arduino model.
* Final power supply and fuse arrangement.

These should be investigated before connecting the motors.

⸻

13. Next Investigation Stage

The next task is to repeat the successful Arduino measurement for the remaining control pins.

Keep:

PIN 4 → Arduino GND

Then measure:

PIN 2 → Arduino analogue input
PIN 3 → Arduino analogue input
PIN 5 → Arduino analogue input

For each pin record:

Neutral
Direction 1
Direction 2

For example:

Pin	Function	Neutral	Direction 1	Direction 2
1	Front base tilt	1023	27–28 DOWN	40–41 UP
2	Rear base tilt	TBD	TBD	TBD
3	Seat forward/back	TBD	TBD	TBD
4	Common	—	—	—
5	Backrest forward/back	TBD	TBD	TBD
6	Unknown	TBD	TBD	TBD

Once this table is complete, we should have the complete switch-input map.

⸻

14. Software Strategy

Do NOT initially write the final motor-control software.

First create a diagnostic Arduino program whose ONLY job is to display the analogue readings.

The diagnostic output should make it easy to establish stable ranges such as:

PIN 1
1023 = neutral
27–28 = front tilt down
40–41 = front tilt up

After all controls have been measured, the final program can translate those readings into commands such as:

FRONT_TILT_DOWN
FRONT_TILT_UP
REAR_TILT_DOWN
REAR_TILT_UP
SEAT_FORWARD
SEAT_BACKWARD
BACKREST_FORWARD
BACKREST_BACKWARD

Only after that decoding stage is proven should the Arduino be connected to motor-driver inputs.

⸻

15. Safety / Testing Rules

At the current stage:

DO NOT connect the 12V seat supply to the Arduino input pins.

The current testing is being performed using the Arduino’s low-voltage USB supply and analogue inputs.

The seat motors should remain completely disconnected while reverse-engineering the switch signals.

Once the control signals are understood, the motor side should be designed separately with:

* appropriate high-current drivers
* correctly sized wiring
* individual motor protection/fusing
* suitable main supply protection
* common ground/reference between Arduino and driver electronics
* software protection against contradictory forward/reverse commands
* sensible maximum run-time/time-out protection

⸻

16. Current Project Status

CONFIRMED:

✓ 4N095747D switch PCB can be used as a standalone input device
✓ Only the top six connector positions are currently relevant
✓ Pin 4 is common
✓ Pin 1 controls front seat-base tilt
✓ Pin 2 controls rear seat-base tilt
✓ Pin 3 controls whole-seat forward/back movement
✓ Pin 5 controls backrest forward/back movement
✓ Direction is not represented simply by different connector pins
✓ Direction produces different analogue readings
✓ PIN 1 has been successfully decoded using Arduino
✓ PIN 1 neutral = ~1023
✓ PIN 1 front tilt DOWN = ~27–28
✓ PIN 1 front tilt UP = ~40–41
✓ Arduino is therefore capable of detecting the original Audi control signals

NOT YET CONFIRMED:

? Exact resistor values
? Remaining analogue values
? PIN 6 function
? Complete motor mapping
? Motor current requirements
? Final H-bridge hardware
? Final Arduino software

⸻

Overall Approach

The project is now being treated as a two-stage system:

STAGE 1 — REVERSE ENGINEER THE CONTROL

Audi switch PCB
      ↓
Arduino analogue inputs
      ↓
Determine every button/direction value
      ↓
Create definitive control map

STAGE 2 — BUILD STANDALONE SEAT CONTROLLER

Audi switch PCB
      ↓
Arduino
      ↓
Motor-driver electronics
      ↓
12V seat motors

The key discovery so far is that the original Audi control switch does not need to be replicated or replaced. We can potentially retain the original OEM switch hardware and use the Arduino as the missing “interpretation” layer between the switch and the seat motors.
