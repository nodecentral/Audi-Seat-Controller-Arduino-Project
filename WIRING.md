# Audi seat controller: enclosure wiring (text version of the diagram)

Use this together with [`images/enclosure-wiring.png`](images/enclosure-wiring.png) (source: [`tools/enclosure_wiring_diagram.py`](tools/enclosure_wiring_diagram.py)). Each row is one physical wire or part.

## Parts
- Arduino Nano (ATmega328) on an HW-152 screw-terminal adapter
- 12V-to-5V buck converter, module C1205003, leads: R = 12V in, B = 0V in, Y = +5V out, B = 0V out (USB lead cut off)
- Cytron MDD10A dual 10A motor driver (no reverse-polarity protection on B+/B-)
- Garosa YYLOCK-2 self-locking delay relay, set to mode P-3 (10-15 min)
- WAGO 221-415 (5-way) used as the ground hub
- Illuminated momentary pushbutton, 5-wire plug: C, NO, NC, LED+, LED-
- J1 and J2: 9-pin 5.08mm pluggable panel terminal blocks
- F1: inline fuse in the +12V feed, F2: 1A inline fuse, R1/R2: 10k resistors

## Terminal labels (as checked)
- **YYLOCK-2 relay block, left to right as mounted:** COM, NO, NC. Source: the maker's labelled product photo.
- **YYLOCK-2 blue DC block, left to right as mounted:** DC+, DC-, IN. Source: the maker's labelled product photo.
- **Cytron control header, left to right:** GND, PWM2, DIR2, PWM1, DIR1. Read off the board's silkscreen.
- **Cytron power/motor block, left to right:** M2B, M2A, B-, B+, M1A, M1B.
  - The M labels were read off the board.
  - The B-/B+ order is taken from Cytron's pinout drawing.
- **Pushbutton wire colours** (red LED+, black LED-, green NO, blue C, yellow NC): read from photos only, NOT from a datasheet. Confirm with a meter before use.

## J1: seat side
| Pin | Signal | Domain |
|---|---|---|
| J1-1 | switch panel PIN 1 (front tilt, parked) | 5V logic |
| J1-2 | switch panel PIN 2 (rear tilt, parked) | 5V logic |
| J1-3 | switch panel PIN 3 (fore/aft) | 5V logic |
| J1-4 | switch panel PIN 5 (recline). Note: PIN 5 is on J1-4 | 5V logic |
| J1-5 | switch panel PIN 4 (switch common ground) | ground |
| J1-6 | pushbutton LED+ (red) | 12V |
| J1-7 | pushbutton NO (green) | 12V |
| J1-8 | pushbutton LED- (black) | ground |
| J1-9 | pushbutton C (blue) | 12V permanent |

Pushbutton NC (yellow) is not used; insulate its end.

## J2: power side
| Pin | Signal |
|---|---|
| J2-1 / J2-2 | recline motor (Cytron M2B / M2A) |
| J2-3 / J2-4 | fore/aft motor (Cytron M1A / M1B) |
| J2-5 | +12V in, permanent vehicle feed, through fuse F1 *before* J2 |
| J2-6 | ground in (chassis) |
| J2-7..9 | spare |

## Wiring list
| # | From | To | Wire | Notes |
|---|---|---|---|---|
| W1 | J1-1 | Nano A1 | 22 AWG | parked axis |
| W2 | J1-2 | Nano A2 | 22 AWG | parked axis |
| W3 | J1-3 | Nano A3 | 22 AWG | |
| W4 | J1-4 | Nano A5 | 22 AWG | |
| W5 | J1-5 | Nano GND (analog-side row) | 22 AWG | |
| W6 | J1-6 | J1-7 | short link on the terminal block | LED+ is fed from the NO line |
| W7 | J1-7 | YYLOCK DC+ | 22 AWG | button powers the module |
| W8 | J1-8 | YYLOCK DC- | 22 AWG | |
| W9 | J1-9 | J2-5 (inside) | 22 AWG | permanent +12V to button C |
| W10 | J2-5 (inside) | YYLOCK COM | 16 AWG | |
| W11 | YYLOCK NO | Cytron B+ | 16 AWG | switched +12V |
| W12 | Cytron B- | WAGO | 16 AWG | |
| W13 | J2-6 (inside) | WAGO | 16 AWG | |
| W14 | Cytron M2B | J2-1 | 16 AWG | |
| W15 | Cytron M2A | J2-2 | 16 AWG | |
| W16 | Cytron M1A | J2-3 | 16 AWG | |
| W17 | Cytron M1B | J2-4 | 16 AWG | |
| W18 | YYLOCK NO | YYLOCK DC+ | 22 AWG | self-latch |
| W19 | YYLOCK DC+ | YYLOCK IN | 22 AWG jumper | mode P-3 trigger |
| W20 | YYLOCK DC- | WAGO | 22 AWG | |
| W21 | YYLOCK NO | F2 (1A), then buck R | 22 AWG | |
| W22 | buck B (input) | WAGO | 22 AWG | |
| W23 | buck Y (+5V out) | Nano 5V | 22 AWG | the only connection to the Nano 5V pin |
| W24 | buck B (output) | Nano GND (analog-side row) | 22 AWG | |
| W25 | Nano D4 | Cytron DIR1 | KF2510 black | |
| W26 | Nano D5 | Cytron PWM1 | KF2510 red | |
| W27 | Nano D7 | Cytron DIR2 | KF2510 white | |
| W28 | Nano D6 | Cytron PWM2 | KF2510 yellow | |
| W29 | Nano GND (digital-side row) | Cytron GND | KF2510 orange | |
| W30 | Nano GND (digital-side row) | WAGO | 22 AWG | |
| R1 | Cytron PWM1 (red wire) | Cytron GND (orange wire) | 10k resistor | soldered at the Cytron plug, heat-shrunk |
| R2 | Cytron PWM2 (yellow wire) | Cytron GND (orange wire) | 10k resistor | soldered at the Cytron plug, heat-shrunk |

## Wires per terminal
| Terminal | Wires |
|---|---|
| YYLOCK DC+ | 3: W7, W18, W19 |
| YYLOCK NO | 3: W11, W18, W21 |
| YYLOCK COM | 1: W10 |
| YYLOCK IN | 1: W19 |
| YYLOCK DC- | 2: W8, W20 |
| J1-7 | 2: W6, W7 |
| J2-5 inside | 2: W9, W10 |
| Nano GND, analog-side row | 2: W5, W24 |
| Nano GND, digital-side row | 2: W29, W30 |
| WAGO | 5 ports: W12, W13, W20, W22, W30 |

## How it works (for checking)
1. **Wake:** at rest nothing has power. Pressing the button connects J1-9 (+12V) to J1-7, putting 12V on YYLOCK DC+. IN is jumpered to DC+, which is a positive trigger per the maker. In P-3 the relay closes at once.
2. **Latch:** NO now carries 12V from COM. W18 feeds it back to DC+, so the module holds itself on after the button is released. NO also powers the Cytron (B+) and, through F2, the buck converter, which powers the Nano.
3. **Auto-off:** after the set time the relay opens. NO drops to 0V, and DC+ loses its feed. Everything is off and draws zero current. The README records this behaviour as bench-tested.
4. **LED:** while latched, DC+ is at 12V. Through W7 and the J1-6/J1-7 link that reaches LED+, so the LED is lit while the system is on.
5. **Control:** the switch panel pulls A3/A5 low through its internal resistors against the Nano's INPUT_PULLUP. The firmware drives DIR/PWM, with an 8 s run cutoff per axis. R1/R2 hold PWM low during the Nano's boot. PWM low means stopped, whatever DIR says (Cytron manual).

## Relay actually fitted (from the bench photo)
- **Marking:** YEYY HZ90-1C12S, DC12V, NO 30A 277VAC/30VDC, NC 20A 277VAC/30VDC.
- **Not the SLA relay:** the maker's product photo and the README show an SLA-12VDC-SL-C relay, which is not what's fitted.
- **Only NO is used.**
- **Rating covers the relay only:** the 30A figure is the relay's. It says nothing about the module's PCB tracks or screw terminals, which is why test T2 exists.

## Why the latch cannot re-energise by itself
- **Two feeds only:** DC+ is fed by the button (W7) and by the relay's own NO through the self-latch (W18). Nothing else.
- **NO needs the relay closed:** NO is only live while the relay is closed. When the timer opens the relay, DC+ loses its feed.
  - The Cytron's and buck converter's capacitors briefly hold DC+ up, but that charge can only decay; there is no source to recharge it.
  - In mode P-3 the relay stays off until power has been fully removed.
- **Button held at timeout:** the module stays powered but the relay stays off. When the button is released, everything is unpowered.
- **No back-feed via the LED:** the LED (J1-6 linked to J1-7, LED- to DC-) only draws current from the DC+ net. It cannot feed it.

## Verification tests (do these before the motors are connected to full power)

### T1: stall current and fuse F1
1. Power one seat motor directly from a fused bench supply or the battery (not through this box). Put an ammeter, or a DC clamp meter, in the feed.
2. Record the running current, then drive the motor to its end stop for no more than 1-2 s and record the stall current. Repeat for the second motor.
3. The firmware allows both axes to move at once, so the worst case is both motors stalled together.

**Pass:**
- each motor's stall current is under the MDD10A's 10A-per-channel continuous rating, with margin
- F1 can be chosen above the combined normal running current plus start-up surge, and at or below what 16 AWG wire is rated for in this install

Use a slow-blow automotive blade fuse, so start-up surges don't blow it.

**Fail:** if stall current is above about 10A per motor, the MDD10A is undersized and the design needs revisiting before going further.

### T2: YYLOCK-2 contacts under load
1. Use a test load that draws roughly the expected motor current (for example a 12V headlamp bulb or a power resistor) in place of the Cytron on NO.
2. Wake the system and leave it latched for the full timeout.
3. Meter the voltage between COM and NO while loaded.

**Pass:**
- the voltage drop is under about 0.1V at 10A
- the relay, the PCB area under it and the screw terminals are only warm, not hot

### T3: latch and timeout behaviour, motors unplugged
Pass if all of these hold:
1. The system wakes on a press and stays on after release.
2. It switches off by itself at the set time, and the J2-5 feed is then the only live point: NO, B+ and the Nano 5V pin all read 0V.
3. It stays off for at least 10 minutes with nobody touching it.
4. Holding the button through the timeout does not leave the motors powered after release.
5. A fresh press starts a fresh cycle.

### T4: pushbutton pinout
Check with the plug fitted and nothing else connected.

Pass if all of these hold:
1. Continuity blue-green only while pressed.
2. Continuity blue-yellow only while released.
3. The meter's diode test lights the LED with + on red. If it lights with + on black instead, swap J1-6 and J1-8.
4. The LED is rated for 12V (marking or listing). Otherwise add a series resistor.

## Open items
- **F1 rating:** set it from the motors' measured stall current. It must not be more than 16 AWG wire can carry. Not decided yet.
- **YYLOCK-2 at stall current:** it's labelled 30A but hasn't been tested at the motors' stall current.
- **Pushbutton:** confirm the wire colours and which LED tab is +, and that the LED is rated for 12V.
- **Enclosure fit:** check the boards fit inside the Hammond 1599HBK. It's tight; measure before drilling.
