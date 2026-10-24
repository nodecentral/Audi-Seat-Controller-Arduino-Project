#!/usr/bin/env python3
# Enclosure wiring diagram generator
# Draws images/enclosure-wiring.svg (and .png if Playwright is installed).
# Layout follows the bench build: Nano (+ buck) | Cytron | WAGO | YYLOCK-2.
# Terminal orders are taken from the boards themselves - see WIRING.md before changing any.
# Usage: python3 tools/enclosure_wiring_diagram.py
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_SVG = os.path.join(HERE, '..', 'images', 'enclosure-wiring.svg')
OUT_PNG = os.path.join(HERE, '..', 'images', 'enclosure-wiring.png')
W, H = 2380, 2440
OX, OY = 330, 110
out = []
def a(s): out.append(s)
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def text(x, y, t, size=13, anchor='start', weight='normal', fill='#222', italic=False, rot=None):
    st = ' font-style="italic"' if italic else ''
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ''
    a(f'<text xml:space="preserve" x="{x}" y="{y}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{tr}>{esc(t)}</text>')
def rpath(pts, r=26):
    import math
    if len(pts) < 3:
        return 'M ' + ' L '.join(f'{x},{y}' for x, y in pts)
    d = f'M {pts[0][0]},{pts[0][1]}'
    for i in range(1, len(pts)-1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i-1], pts[i], pts[i+1]
        l1 = math.hypot(x1-x0, y1-y0) or 1; l2 = math.hypot(x2-x1, y2-y1) or 1
        rr = min(r, l1/2, l2/2)
        ax, ay = x1 - (x1-x0)/l1*rr, y1 - (y1-y0)/l1*rr
        bx, by = x1 + (x2-x1)/l2*rr, y1 + (y2-y1)/l2*rr
        d += f' L {ax:.1f},{ay:.1f} Q {x1},{y1} {bx:.1f},{by:.1f}'
    d += f' L {pts[-1][0]},{pts[-1][1]}'
    return d
def wire(pts, color, w=4.5, dash=None, r=None):
    d = rpath(pts, r if r else (22 if w < 6 else 30))
    a(f'<path d="{d}" fill="none" stroke="#00000075" stroke-width="{w+2.8}" stroke-linejoin="round" stroke-linecap="round"/>')
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{ds}/>')
    a(f'<path d="{d}" fill="none" stroke="#ffffff38" stroke-width="{max(1.2, w/3.5)}" stroke-linecap="round" transform="translate(-0.8,-0.8)"/>')
    for (ex, ey) in (pts[0], pts[-1]):
        a(f'<circle cx="{ex}" cy="{ey}" r="{w/2+1.5}" fill="#d9d9d9" stroke="#555" stroke-width="1"/>')
def curve(p0, c1, c2, p1, color, w=4):
    d = f'M {p0[0]},{p0[1]} C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {p1[0]},{p1[1]}'
    a(f'<path d="{d}" fill="none" stroke="#00000070" stroke-width="{w+2.6}" stroke-linecap="round"/>')
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
def pin(x, y, label=None, side='r', used=True, size=11):
    fill = '#c9a227' if used else '#8d8d8d'
    a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{fill}" stroke="#444" stroke-width="1.2"/>')
    a(f'<line x1="{x-3.5}" y1="{y}" x2="{x+3.5}" y2="{y}" stroke="#444" stroke-width="1.4"/>')
    if label:
        col = '#fff' if used else '#b0bec5'; wt = 'bold' if used else 'normal'
        if side == 'r': text(x+11, y+4, label, size, 'start', wt, col)
        elif side == 'l': text(x-11, y+4, label, size, 'end', wt, col)
        elif side == 'b': text(x, y+21, label, size, 'middle', wt, col)
        elif side == 't': text(x, y-12, label, size, 'middle', wt, col)
def board(x, y, w, h, fill, rx=8):
    a(f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" rx="{rx}" fill="#00000035"/>')
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#00000090" stroke-width="2"/>')
    for hx, hy in [(x+11, y+11), (x+w-11, y+11), (x+11, y+h-11), (x+w-11, y+h-11)]:
        a(f'<circle cx="{hx}" cy="{hy}" r="5" fill="#e0e0e0" stroke="#777"/>')

P12, S12, GND, V5 = '#d00000', '#e0457b', '#1a1a1a', '#8a3ffc'
SIG, PARK = '#2a9d8f', '#8fbcb5'
MOT1, MOT2 = '#1d4e89', '#4f8cc9'

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>')
text(W/2, 44, 'Audi seat controller - enclosure wiring (bench layout, buck beside the Nano)', 27, 'middle', 'bold')
text(W/2, 72, 'Hammond 1599HBK  |  J1 seat side: switch panel + pushbutton (9-pin)  |  J2 power side: 12V in + 2 motor outputs (9-pin)  |  not to scale', 15, 'middle', 'normal', '#444')
a(f'<g transform="translate({OX},{OY})">')

BX1, BY1 = 1640, 1010
a(f'<rect x="0" y="0" width="{BX1}" height="{BY1}" rx="24" fill="#3a3a3c" stroke="#1c1c1e" stroke-width="6"/>')
a(f'<rect x="16" y="16" width="{BX1-32}" height="{BY1-32}" rx="16" fill="#505054" stroke="#2a2a2c" stroke-width="2"/>')

# ---- terminal blocks
J1 = {i+1: (0, 250 + i*40) for i in range(9)}
J2 = {i+1: (BX1, 250 + i*40) for i in range(9)}
def tblock(pins, x, name):
    ys = [p[1] for p in pins.values()]; y0, y1 = min(ys)-28, max(ys)+28
    a(f'<rect x="{x-42}" y="{y0}" width="84" height="{y1-y0}" rx="5" fill="#2e8b3e" stroke="#1d5c28" stroke-width="2"/>')
    for n, (px, py) in pins.items():
        a(f'<rect x="{x-36}" y="{py-17}" width="72" height="34" rx="3" fill="#38a84b" stroke="#1d5c28"/>')
        for sx in (x-18, x+18):
            a(f'<circle cx="{sx}" cy="{py}" r="9.5" fill="#c0c0c0" stroke="#666" stroke-width="1.5"/>')
            a(f'<line x1="{sx-6}" y1="{py}" x2="{sx+6}" y2="{py}" stroke="#555" stroke-width="2.2"/>')
    return y1
J1b = tblock(J1, 0, 'J1'); J2b = tblock(J2, BX1, 'J2')
JI1 = lambda n: (42, J1[n][1])        # inside contact of J1
JI2 = lambda n: (BX1-42, J2[n][1])    # inside contact of J2

# ---- Nano on HW-152 (USB at top, analog row on the left - as on the bench)
NX0, NY0, NX1, NY1 = 170, 150, 410, 590
board(NX0, NY0, NX1-NX0, NY1-NY0, '#1565c0')
a(f'<rect x="{NX0+55}" y="{NY0+36}" width="{NX1-NX0-110}" height="{NY1-NY0-72}" rx="4" fill="#0d47a1" stroke="#00000080"/>')
a(f'<rect x="{(NX0+NX1)/2-18}" y="{NY0+22}" width="36" height="26" rx="3" fill="#b0b0b0" stroke="#666"/>')
a(f'<rect x="{(NX0+NX1)/2-20}" y="{330}" width="40" height="40" fill="#212121" transform="rotate(45 {(NX0+NX1)/2} 350)"/>')
text((NX0+NX1)/2, 430, 'ARDUINO', 15, 'middle', 'bold', '#fff'); text((NX0+NX1)/2, 448, 'NANO', 15, 'middle', 'bold', '#fff')
text((NX0+NX1)/2, 466, 'on HW-152', 11, 'middle', 'normal', '#cfd8dc', italic=True)
Ln = ['D13', '3V3', 'REF', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', '5V', 'RST', 'GND', 'VIN']
Rn = ['D12', 'D11', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'GND', 'RST', 'RX0', 'TX1']
NL = {n: (NX0+18, 190 + i*27) for i, n in enumerate(Ln)}
NR = {n: (NX1-18, 190 + i*27) for i, n in enumerate(Rn)}

# ---- buck under the Nano
KX0, KY0, KX1, KY1 = 180, 650, 400, 790
board(KX0, KY0, KX1-KX0, KY1-KY0, '#37474f')
text((KX0+KX1)/2, 712, 'BUCK 12V -> 5V', 15, 'middle', 'bold', '#fff')
text((KX0+KX1)/2, 730, 'C1205003 (USB lead cut off)', 11, 'middle', 'normal', '#cfd8dc', italic=True)
BK = {'Y +5V': (205, KY0+14), 'B 0V': (250, KY0+14), 'R 12V': (330, KY1-14), 'B in': (375, KY1-14)}

# ---- Cytron MDD10A: power/motor terminals TOP, KF2510 header BOTTOM (as on bench)
CX0, CY0, CX1, CY1 = 480, 150, 800, 720
board(CX0, CY0, CX1-CX0, CY1-CY0, '#202020')
a(f'<rect x="{CX0+12}" y="{CY0+2}" width="{CX1-CX0-24}" height="26" rx="3" fill="#111" stroke="#555"/>')
a(f'<rect x="618" y="{CY0+2}" width="64" height="26" rx="3" fill="#2e8b57" stroke="#1d5c38"/>')
for cx, cy in [(600, 330), (680, 330), (600, 400), (680, 400)]:
    a(f'<circle cx="{cx}" cy="{cy}" r="24" fill="#bdbdbd" stroke="#777"/>'); a(f'<circle cx="{cx}" cy="{cy}" r="17" fill="#9e9e9e"/>')
text(640, 480, 'CYTRON', 17, 'middle', 'bold', '#fff'); text(640, 500, 'MDD10A', 17, 'middle', 'bold', '#fff')
text(640, 520, 'dual 10A motor driver', 11, 'middle', 'normal', '#bbb', italic=True)
CT = {n: (x, CY0+15) for n, x in [('M2B', 510), ('M2A', 565), ('B-', 630), ('B+', 670), ('M1A', 735), ('M1B', 785)]}
a(f'<rect x="570" y="{CY1-30}" width="140" height="28" rx="3" fill="#fafafa" stroke="#999"/>')
CH = {n: (x, CY1-16) for n, x in [('GND', 585), ('PWM2', 612), ('DIR2', 640), ('PWM1', 668), ('DIR1', 695)]}

# ---- WAGO 221 (5-way), between Cytron and YYLOCK at the top
WX0, WY0 = 860, 150
a(f'<rect x="{WX0}" y="{WY0}" width="118" height="86" rx="6" fill="#f5f5f5" stroke="#888" stroke-width="2"/>')
for i in range(5):
    a(f'<rect x="{WX0+6+i*22}" y="{WY0+8}" width="18" height="50" rx="3" fill="#ff9800" stroke="#c66900"/>')
text(WX0+59, WY0+76, 'WAGO 221', 11, 'middle', 'bold', '#555')
WP = [(WX0+15+i*22, WY0+86) for i in range(5)]   # wire entries face down

# ---- YYLOCK-2: relay terminals TOP, DC terminal block BOTTOM (as on bench)
YX0, YY0, YX1, YY1 = 1040, 150, 1360, 720
board(YX0, YY0, YX1-YX0, YY1-YY0, '#1b7a3d')
a(f'<rect x="1080" y="{YY0+2}" width="240" height="30" rx="3" fill="#222" stroke="#555"/>')
a(f'<rect x="1120" y="300" width="150" height="150" rx="4" fill="#111" stroke="#444"/>')
text(1195, 360, 'YEYY relay', 13, 'middle', 'bold', '#ddd'); text(1195, 378, 'HZ90-1C12S 30A', 11, 'middle', 'normal', '#aaa')
text(1200, 500, 'YYLOCK-2', 17, 'middle', 'bold', '#fff'); text(1200, 520, 'power latch, mode P-3', 12, 'middle', 'normal', '#e0f2e9', italic=True)
text(1200, 537, '10-15 min auto-off', 12, 'middle', 'normal', '#e0f2e9', italic=True)
a(f'<rect x="1120" y="{YY1-32}" width="160" height="30" rx="3" fill="#1e88e5" stroke="#0d47a1"/>')
YR = {n: (x, YY0+17) for n, x in [('COM', 1120), ('NO', 1200), ('NC', 1280)]}   # confirmed from product image
YD = {n: (x, YY1-17) for n, x in [('DC+', 1145), ('DC-', 1200), ('IN', 1255)]}   # confirmed from product image

# ================= wires =================
# --- switch panel -> Nano analog row (J1-4 = PIN5, J1-5 = PIN4 so nothing crosses)
wire([JI1(1), (150, J1[1][1]), (150, NL['A1'][1]), NL['A1']], PARK, 4, '10 6')
wire([JI1(2), (138, J1[2][1]), (138, NL['A2'][1]), NL['A2']], PARK, 4, '10 6')
wire([JI1(3), (126, J1[3][1]), (126, NL['A3'][1]), NL['A3']], SIG, 4)
wire([JI1(4), (114, J1[4][1]), (114, NL['A5'][1]), NL['A5']], '#43aa8b', 4)
wire([JI1(5), (102, J1[5][1]), (102, NL['GND'][1]-3), (NL['GND'][0], NL['GND'][1]-3)], GND, 4)
a(f'<path d="M 30,{J1[6][1]} C 54,{J1[6][1]+8} 54,{J1[7][1]-8} 30,{J1[7][1]}" fill="none" stroke="#e0457b" stroke-width="4"/>')
text(58, J1[6][1]+24, 'link', 10, 'start', 'bold', '#ffd6e5')
# --- buck out -> Nano 5V / GND
wire([BK['Y +5V'], (205, 625), (150, 625), (150, NL['5V'][1]), NL['5V']], V5, 4)
wire([BK['B 0V'], (250, 612), (162, 612), (162, NL['GND'][1]+4), (NL['GND'][0], NL['GND'][1]+4)], GND, 4)
# --- Nano -> Cytron KF2510 (real colours), entering the header from below
for n, c, col, lane in [('D7', 'DIR2', '#f5f5f5', 752), ('D6', 'PWM2', '#fdd835', 764), ('D5', 'PWM1', '#e53935', 776), ('D4', 'DIR1', '#111111', 788), ('GND', 'GND', '#fb8c00', 800)]:
    x0, y0 = NR[n]; x1, y1 = CH[c]
    curve((x0, y0-(3 if n == 'GND' else 0)), (480, y0), (450, lane+10), (510, lane), col, 3.5)
    wire([(510, lane), (x1, lane), (x1, y1)], col, 3.5)
# --- WAGO ground wires
wire([(NR['GND'][0], NR['GND'][1]+4), (408, NR['GND'][1]+4), (408, 845), (WP[1][0], 845), WP[1]], GND, 4)    # Nano GND
wire([BK['B in'], (375, 860), (WP[2][0], 860), WP[2]], GND, 4)                                               # buck IN-
wire([CT['B-'], (630, 98), (845, 98), (845, 270), (WP[0][0], 270), WP[0]], GND, 7)                           # Cytron B-
wire([(YD['DC-'][0]-6, YD['DC-'][1]+4), (YD['DC-'][0]-6, 875), (WP[4][0], 875), WP[4]], GND, 4)                                       # YYLOCK DC-
wire([JI2(6), (1480, J2[6][1]), (1480, 890), (WP[3][0], 890), WP[3]], GND, 7)                                # GND IN
# --- motors -> J2 1-4 (16 AWG), over the top
wire([CT['M2B'], (510, 34), (1580, 34), (1580, J2[1][1]), JI2(1)], MOT2, 7)
wire([CT['M2A'], (565, 50), (1564, 50), (1564, J2[2][1]), JI2(2)], MOT2, 7, '14 5')
wire([CT['M1A'], (735, 66), (1548, 66), (1548, J2[3][1]), JI2(3)], MOT1, 7)
wire([CT['M1B'], (785, 82), (1532, 82), (1532, J2[4][1]), JI2(4)], MOT1, 7, '14 5')
# --- switched 12V out of NO: Cytron B+, buck, self-latch
NOX, NOY = YR['NO']
wire([CT['B+'], (670, 112), (NOX+12, 112), (NOX+12, NOY-8), (NOX, NOY)], S12, 7)                         # NO -> B+ (16 AWG)
wire([(NOX, NOY), (NOX, NOY-8), (NOX, 124), (1006, 124), (1006, 910), (BK['R 12V'][0], 910), BK['R 12V']], S12, 4)   # NO -> buck IN+
wire([(NOX, NOY), (NOX-12, NOY-8), (NOX-12, 136), (1022, 136), (1022, 790), (YD['DC+'][0], 790), YD['DC+']], S12, 4)  # self-latch NO -> DC+
a(f'<path d="M {YD["DC+"][0]},{YD["DC+"][1]+2} C {YD["DC+"][0]+10},{YY1+24} {YD["IN"][0]-10},{YY1+24} {YD["IN"][0]},{YD["IN"][1]+2}" fill="none" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="3 4"/>')
# --- power in: J2-5 +12V -> COM
wire([(BX1-42, J2[5][1]-5), (1500, J2[5][1]-5), (1500, 148), (YR['COM'][0], 148), YR['COM']], P12, 7)
# --- pushbutton
wire([JI1(7), (92, J1[7][1]), (92, 930), (YD['DC+'][0]+5, 930), (YD['DC+'][0]+5, YD['DC+'][1]+4)], P12, 4)     # button NO -> DC+
wire([JI1(8), (80, J1[8][1]), (80, 945), (YD['DC-'][0]+6, 945), (YD['DC-'][0]+6, YD['DC-'][1]+4)], GND, 4)      # LED- -> DC-
wire([JI1(9), (68, J1[9][1]), (68, 960), (1460, 960), (1460, J2[5][1]+5), (BX1-42, J2[5][1]+5)], P12, 4)       # C <- J2-5 +12V
# ---- fuse, pull-down, polarity and callout markers
def fuse(x, y, label, vertical=True, sub=None):
    if vertical:
        a(f'<rect x="{x-11}" y="{y-24}" width="22" height="48" rx="6" fill="#fff3bf" stroke="#7a5d00" stroke-width="2"/>')
        a(f'<line x1="{x}" y1="{y-18}" x2="{x}" y2="{y+18}" stroke="#7a5d00" stroke-width="2"/>')
    else:
        a(f'<rect x="{x-24}" y="{y-11}" width="48" height="22" rx="6" fill="#fff3bf" stroke="#7a5d00" stroke-width="2"/>')
        a(f'<line x1="{x-18}" y1="{y}" x2="{x+18}" y2="{y}" stroke="#7a5d00" stroke-width="2"/>')
def marker(x, y, n):
    a(f'<circle cx="{x}" cy="{y}" r="15" fill="#ffcc00" stroke="#111" stroke-width="2"/>')
    text(x, y+5, str(n), 15, 'middle', 'bold', '#111')
fuse(BK['R 12V'][0], 866, 'F2')
text(BK['R 12V'][0]-18, 870, 'F2 1A', 12, 'end', 'bold', '#ffe066')
# pull-down badge on the KF2510 cable near the Cytron plug
a('<rect x="600" y="806" width="150" height="30" rx="6" fill="#fff3bf" stroke="#7a5d00" stroke-width="1.5"/>')
text(675, 826, 'R1 R2 10k pull-downs', 11, 'middle', 'bold', '#5a4500')
marker(586, 821, 4)
# YYLOCK callout
a('<rect x="1060" y="560" width="280" height="96" rx="8" fill="#0f5a2b" stroke="#bfe8cc"/>')
for i, t in enumerate(['Button powers the module: pressed, it', 'puts 12V on DC+. IN is jumpered to DC+', '(positive trigger). Mode P-3: relay on for', 'the set time, then off. Bench-tested.']):
    text(1200, 580+i*19, t, 12, 'middle', 'normal', '#e8fff0')
marker(1050, 558, 1)
# polarity on Cytron supply
for nm, sym in (('B+', '+'), ('B-', '−')):
    x, y = CT[nm]
    a(f'<circle cx="{x}" cy="{y+44}" r="11" fill="{"#d00000" if sym == "+" else "#111"}" stroke="#fff" stroke-width="1.5"/>')
    text(x, y+49, sym, 15, 'middle', 'bold', '#fff')
marker(652, 236, 3)
text(652, 270, 'no reverse-polarity', 11, 'middle', 'bold', '#ffb3b3')
text(652, 284, 'protection', 11, 'middle', 'bold', '#ffb3b3')
marker(WX0+59, WY0+112, 6)
# ---- pins on top
usedL = {'A1', 'A2', 'A3', 'A5', '5V', 'GND'}; usedR = {'D4', 'D5', 'D6', 'D7', 'GND'}
for n, p in NL.items(): pin(*p, n, 'r', n in usedL)
for n, p in NR.items(): pin(*p, n, 'l', n in usedR)
for n, p in BK.items(): pin(*p, n, 'b' if p[1] < 700 else 't', True, 10)
for n, p in CT.items(): pin(*p, n, 'b', True, 11)
for n, p in CH.items(): pin(*p, None, 'b', True)
for n, (x, y) in CH.items(): text(x, y-18, n, 9, 'middle', 'bold', '#fff', rot=-60)
for n, p in YR.items(): pin(*p, n, 'b', n != 'NC')
for n, p in YD.items(): pin(*p, n, 't', True)
text(1200, YY1+40, 'IN-DC+ jumper', 10, 'middle', 'normal', '#ddd', italic=True)
for i, p in enumerate(WP): a(f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="#555"/>')

# ---- terminal labels (outside)
ext1 = [('Switch PIN 1', 'front tilt - parked (A1)', PARK, True), ('Switch PIN 2', 'rear tilt - parked (A2)', PARK, True),
        ('Switch PIN 3', 'fore / aft (A3)', SIG, False), ('Switch PIN 5', 'recline (A5)', '#43aa8b', False),
        ('Switch PIN 4', 'switch common GND -> Nano GND', GND, False), ('Pushbutton LED +  (red)', 'linked to J1-7 on the block', '#e53935', False),
        ('Pushbutton NO  (green)', '-> YYLOCK DC+', '#16a34a', False), ('Pushbutton LED -  (black)', '-> YYLOCK DC-', '#111111', False),
        ('Pushbutton C  (blue)', '+12V permanent (from J2-5)', '#1e63d6', False)]
a('<rect x="-330" y="228" width="292" height="204" rx="8" fill="#e6f4f1"/>')
a('<rect x="-330" y="468" width="292" height="164" rx="8" fill="#fdecec"/>')
for i, (nm, ds, col, dash) in enumerate(ext1, 1):
    x, y = J1[i]
    wire([(x-30, y), (x-105, y)], col, 4, '10 6' if dash else None)
    text(x-115, y-1, f'{i}  {nm}', 13, 'end', 'bold'); text(x-115, y+14, ds, 11, 'end', 'normal', '#555', True)
a('<path d="M -300,228 L -312,228 L -312,432 L -300,432" fill="none" stroke="#777" stroke-width="2"/>')
text(-320, 330, 'SWITCH PANEL - 5V LOGIC ONLY', 12, 'middle', 'bold', '#1b6b5c', rot=-90)
a('<path d="M -300,468 L -312,468 L -312,632 L -300,632" fill="none" stroke="#777" stroke-width="2"/>')
text(-320, 550, 'BUTTON - 12V ONLY', 12, 'middle', 'bold', '#a32020', rot=-90)
ext2 = [('Recline motor A', 'Cytron M2B', MOT2, 7), ('Recline motor B', 'Cytron M2A', MOT2, 7), ('Fore/aft motor A', 'Cytron M1A', MOT1, 7),
        ('Fore/aft motor B', 'Cytron M1B', MOT1, 7), ('+12V IN  (+)', 'from fuse F1, permanent feed', P12, 7), ('GND IN  (−)', 'chassis ground', GND, 7),
        ('spare', 'e.g. 2nd Cytron later', None, 0), ('spare', '', None, 0), ('spare', '', None, 0)]
for i, (nm, ds, col, w) in enumerate(ext2, 1):
    x, y = J2[i]
    if w: wire([(x+30, y), (x+105, y)], col, w)
    text(x+115, y-1, f'{i}  {nm}', 13, 'start', 'bold', '#222' if w else '#999')
    if ds: text(x+115, y+14, ds, 11, 'start', 'normal', '#555', True)
for x, name in [(0, 'J1  SEAT SIDE'), (BX1, 'J2  POWER SIDE')]:
    a(f'<rect x="{x-72}" y="{J1b+6}" width="144" height="26" rx="6" fill="#1d5c28"/>')
    text(x, J1b+24, name, 14, 'middle', 'bold', '#fff')
fuse(BX1+68, J2[5][1], 'F1', vertical=False)
text(BX1+68, J2[5][1]-18, 'F1', 12, 'middle', 'bold', '#7a5d00')
marker(BX1+320, J2[5][1]+4, 2)
marker(-312, 450, 5)
a('</g>')

# ================= panels below the diagram =================
LY = OY + BY1 + 44
items = [(P12, 'permanent +12V', 5, None), (S12, 'switched +12V (only while latched)', 5, None), (V5, '+5V', 5, None), (GND, 'ground', 5, None),
         (SIG, 'switch signal (5V logic)', 5, None), (PARK, 'parked axis', 5, '10 6'), (MOT1, 'motor / B+ / B- / 12V in: 16 AWG', 8, None)]
x = 60
for col, lab, w, dash in items:
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<line x1="{x}" y1="{LY}" x2="{x+44}" y2="{LY}" stroke="#00000066" stroke-width="{w+2.5}" stroke-linecap="round"/>')
    a(f'<line x1="{x}" y1="{LY}" x2="{x+44}" y2="{LY}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{ds}/>')
    text(x+54, LY+5, lab, 13); x += 80 + len(lab)*7.3
text(60, LY+30, 'Inside the box wires are coloured by job. Outside J1 they are the pushbutton\'s real wire colours. Thin wires are 22 AWG; the KF2510 cable is 26 AWG. Not to scale.', 13, 'start', 'normal', '#333')

def panel(x, y, w, h, title, n=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="#bbb" stroke-width="1.5"/>')
    if n is not None:
        a(f'<circle cx="{x+24}" cy="{y+24}" r="14" fill="#ffcc00" stroke="#111" stroke-width="2"/>'); text(x+24, y+29, str(n), 14, 'middle', 'bold', '#111')
    text(x+(46 if n is not None else 18), y+30, title, 16, 'start', 'bold', '#222')

# ---- wiring list (left)
PY = LY + 60
rows = [
 ('Switch panel to Nano  (22 AWG, 5V logic only)', None),
 ('W1', 'J1-1  switch PIN 1', 'Nano A1', 'parked - front tilt, no driver yet'),
 ('W2', 'J1-2  switch PIN 2', 'Nano A2', 'parked - rear tilt, no driver yet'),
 ('W3', 'J1-3  switch PIN 3', 'Nano A3', 'fore / aft'),
 ('W4', 'J1-4  switch PIN 5', 'Nano A5', 'recline  (note: PIN 5 on J1-4)'),
 ('W5', 'J1-5  switch PIN 4', 'Nano GND (analog row)', 'switch common'),
 ('Pushbutton  (22 AWG, 12V only - never to a Nano pin)', None),
 ('W6', 'J1-6  (red, LED+)', 'J1-7  short link on the block', 'LED fed from the NO line'),
 ('W7', 'J1-7  (green, NO)', 'YYLOCK DC+', 'button powers the module'),
 ('W8', 'J1-8  (black, LED-)', 'YYLOCK DC-', ''),
 ('W9', 'J1-9  (blue, C)', 'J2-5 (inside)', 'permanent +12V for the button'),
 ('12V power and motors  (16 AWG)', None),
 ('W10', 'J2-5  +12V in', 'YYLOCK COM', 'feed is fused at F1 before J2'),
 ('W11', 'YYLOCK NO', 'Cytron B+', 'switched +12V - check polarity'),
 ('W12', 'Cytron B-', 'WAGO port', 'check polarity'),
 ('W13', 'J2-6  GND in', 'WAGO port', ''),
 ('W14-15', 'Cytron M2B / M2A', 'J2-1 / J2-2', 'recline motor'),
 ('W16-17', 'Cytron M1A / M1B', 'J2-3 / J2-4', 'fore / aft motor'),
 ('YYLOCK-2 and buck converter  (22 AWG)', None),
 ('W18', 'YYLOCK NO', 'YYLOCK DC+', 'self-latch'),
 ('W19', 'YYLOCK DC+', 'YYLOCK IN', 'jumper - mode P-3 trigger'),
 ('W20', 'YYLOCK DC-', 'WAGO port', ''),
 ('W21', 'YYLOCK NO', 'F2 (1A)  then buck R (12V in)', 'buck lead, fused'),
 ('W22', 'Buck B (input -)', 'WAGO port', ''),
 ('W23', 'Buck Y (+5V out)', 'Nano 5V', 'never 12V on this pin'),
 ('W24', 'Buck B (output -)', 'Nano GND (analog row)', ''),
 ('Nano to Cytron  (KF2510 cable, 26 AWG)', None),
 ('W25', 'Nano D4', 'Cytron DIR1', 'black'),
 ('W26', 'Nano D5', 'Cytron PWM1', 'red'),
 ('W27', 'Nano D7', 'Cytron DIR2', 'white'),
 ('W28', 'Nano D6', 'Cytron PWM2', 'yellow'),
 ('W29', 'Nano GND (digital row)', 'Cytron GND', 'orange'),
 ('W30', 'Nano GND (digital row)', 'WAGO port', '22 AWG'),
 ('R1', 'Cytron PWM1 (red)', 'Cytron GND (orange)', '10k pull-down at the plug'),
 ('R2', 'Cytron PWM2 (yellow)', 'Cytron GND (orange)', '10k pull-down at the plug'),
]
TW = 1220
nrow = len(rows)
panel(40, PY, TW, 70 + nrow*24, 'Wiring list - tick each one off as you wire it')
cols = [(60, '#'), (150, 'From'), (450, 'To'), (790, 'Notes')]
for cx, h in cols: text(cx, PY+58, h, 13, 'start', 'bold', '#555')
a(f'<line x1="56" y1="{PY+66}" x2="{40+TW-16}" y2="{PY+66}" stroke="#ccc"/>')
y = PY + 88
for r in rows:
    if r[1] is None:
        a(f'<rect x="52" y="{y-16}" width="{TW-24}" height="22" rx="4" fill="#eef2f6"/>')
        text(60, y, r[0], 13, 'start', 'bold', '#1d3557')
    else:
        a(f'<rect x="{1220}" y="{y-13}" width="14" height="14" rx="2" fill="#fff" stroke="#888"/>')
        for (cx, _), v in zip(cols, r): text(cx, y, v, 13, 'start', 'bold' if cx == 60 else 'normal', '#222')
    y += 24
LIST_END = y

# ---- right column panels
RX, RW = 1290, 1050
# pushbutton
P1 = PY
panel(RX, P1, RW, 250, 'Pushbutton rear view - 5-wire plug (colours read from your photos)', 5)
IX, IY = RX+170, P1+140
a(f'<circle cx="{IX}" cy="{IY}" r="72" fill="#2f6fd6" stroke="#174a9a" stroke-width="3"/>')
a(f'<rect x="{IX-60}" y="{IY-27}" width="120" height="40" rx="6" fill="#d7d7d0" stroke="#999"/>')
tabs = {'LEDt': (IX+30, IY-67), 'NC': (IX-40, IY-9), 'NO': (IX, IY-9), 'C': (IX+40, IY-9), 'LEDb': (IX-10, IY+61)}
leads = [('LEDt', '#e53935', IY-67, 'red     LED top tab   ->  J1-6  (LED+)'),
         ('NC', '#f2c200', IY-43, 'yellow  NC            ->  not used - insulate the end'),
         ('NO', '#16a34a', IY-21, 'green   NO            ->  J1-7'),
         ('C', '#1e63d6', IY+25, 'blue    C             ->  J1-9'),
         ('LEDb', '#111111', IY+61, 'black   LED bottom tab ->  J1-8  (LED-)')]
for k, (tx, ty) in tabs.items():
    w_, h_ = (8, 26) if k in ('NC', 'NO', 'C') else (18, 9)
    a(f'<rect x="{tx-w_/2}" y="{ty-h_/2}" width="{w_}" height="{h_}" fill="#c8c8c8" stroke="#555"/>')
for k, col, ly, lab in leads:
    tx, ty = tabs[k]
    if k in ('NC', 'NO'): pts = [(tx, ty-13), (tx, ly), (IX+120, ly)]
    elif k == 'C': pts = [(tx, ty+13), (tx, ly), (IX+120, ly)]
    else: pts = [(tx+9, ty), (IX+120, ty)]
    wire(pts, col, 3.5, r=10)
    text(IX+130, ly+5, lab, 13, 'start', 'normal', '#333')
text(RX+RW/2, P1+236, 'Not from a datasheet - confirm with a meter (checklist step 1) before relying on it.', 12, 'middle', 'bold', '#a32020')

# safety notes
P2 = P1 + 270
notes = [
 (1, 'YYLOCK-2 trigger.', 'The button does not signal the Nano. Pressing it puts +12V on the module\'s own DC+ supply; IN is jumpered to DC+ (the maker lists IN as a', 'positive, high-level trigger). In mode P-3 the relay closes at once, stays on for the set time, then opens and stays off. Bench-tested (README).'),
 (2, 'Fuses.', 'F1 sits in the +12V feed before J2-5, as close to the supply as possible. Its rating is set from the motors\' measured stall current and must not', 'exceed what 16 AWG wire can carry - not yet decided (README open item). F2 is 1A on the buck converter\'s red input lead.'),
 (3, 'Polarity.', 'The Cytron MDD10A has no reverse-polarity protection: B+ must get the switched +12V from YYLOCK NO, B- must go to ground. Check before', 'power-up. The YYLOCK relay is labelled 30A, but the module has not been tested at the motors\' stall current yet.'),
 (4, 'No movement at start-up.', 'For about a second while the Nano boots, D5/D6 float. R1/R2 (10k) hold PWM1/PWM2 low, and PWM low = motor stopped whatever DIR', 'is (Cytron manual). Solder them across the cable wires at the Cytron plug and heat-shrink. The firmware then drives the pins LOW in setup().'),
 (5, 'Two separate groups on J1.', 'J1-1 to J1-5: switch panel, 5V logic, to the Nano. J1-6 to J1-9: pushbutton, 12V, to the YYLOCK/J2 only. No pushbutton wire', 'goes to a Nano pin. The only thing on the Nano\'s 5V pin is the buck converter\'s regulated 5V output.'),
 (6, 'Grounds.', 'All grounds meet at the WAGO (5 ports): Cytron B-, Nano GND, buck input -, J2-6 GND in, YYLOCK DC-. Nano analog-row GND: switch PIN 4 +', 'buck output -. Nano digital-row GND: KF2510 orange + wire to the WAGO. YYLOCK DC-: WAGO wire + button LED-.'),
]
panel(RX, P2, RW, 60 + len(notes)*64, 'Safety notes - numbered markers on the diagram')
yy = P2 + 62
for n, head, l1, l2 in notes:
    a(f'<circle cx="{RX+28}" cy="{yy-5}" r="13" fill="#ffcc00" stroke="#111" stroke-width="2"/>'); text(RX+28, yy, str(n), 13, 'middle', 'bold', '#111')
    text(RX+52, yy, head, 13, 'start', 'bold', '#222')
    text(RX+52, yy+19, l1, 12, 'start', 'normal', '#333')
    text(RX+52, yy+36, l2, 12, 'start', 'normal', '#333')
    yy += 64

# conductors per terminal
P3 = P2 + 60 + len(notes)*64 + 20
cpt = ['YYLOCK DC+: 3 (button NO, self-latch, IN jumper)   |   YYLOCK NO: 3 (Cytron B+, self-latch, F2/buck)   |   COM: 1   |   IN: 1 (jumper)',
       'YYLOCK DC-: 2 (WAGO, LED-)   |   J1-7: 2 (button NO, link)   |   J2-5 inside: 2 (COM, button C)   |   Nano GND pins: 2 each   |   WAGO: 1 per port']
panel(RX, P3, RW, 92, 'Wires per screw terminal (count them when you check)')
for i, t in enumerate(cpt): text(RX+18, P3+56+i*20, t, 12, 'start', 'normal', '#333')

# checklist
P4 = P3 + 112
steps = [
 '1  Button: with the plug on, meter blue-green beeps only while pressed; blue-yellow beeps when released. Diode test red/black to find LED +.',
 '2  Check every row of the wiring list by continuity, terminal to terminal, and tick it. Tug-test every screw terminal and WAGO lever.',
 '3  No supply connected: J2-5 to J2-6 must NOT read near 0 ohms. Cytron B+ to B- must not read near 0 ohms.',
 '4  Fit F1 (rating decided from stall current) and F2 (1A). Confirm the vehicle feed polarity at the J2 plug before connecting it.',
 '5  First power-up with motor plugs J2-1..4 disconnected: press the button - relay clicks, Nano LED on, Nano 5V pin reads 4.75-5.25V.',
 '6  Still without motors: meter M1A-M1B and M2A-M2B read 0V at rest, about 12V only while a seat switch is held, 0V again on release.',
 '7  Connect the motors and test each direction; confirm the 8 s run cutoff and that the YYLOCK switches everything off after its set time.',
]
panel(40, LIST_END + 20, TW, 60 + len(steps)*24, 'Before the first power-up')
yy = LIST_END + 20 + 58
for t in steps:
    a(f'<rect x="{TW+0}" y="{yy-13}" width="14" height="14" rx="2" fill="#fff" stroke="#888"/>')
    text(60, yy, t, 12, 'start', 'normal', '#222'); yy += 24
END = max(yy, P4) + 20
a('</svg>')
open(OUT_SVG, 'w').write('\n'.join(out))
print('wrote', os.path.normpath(OUT_SVG))
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': W, 'height': H})
        page.goto('file://' + os.path.abspath(OUT_SVG))
        page.screenshot(path=OUT_PNG)
        browser.close()
    print('wrote', os.path.normpath(OUT_PNG))
except ImportError:
    print('Playwright not installed - PNG not regenerated (open the SVG in a browser instead)')
