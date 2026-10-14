"""Sound design for "Your business has amnesia" (45 s, loops).

Original synthesized music and effects, timed from the timeline the animation exports.
The AI voice line (T.voice to T.voiceEnd) is left clear so the real product recording can be dropped in.

    python3 sound.py timeline_v.json out.wav [voice.wav]
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
tl = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
VOICE = sys.argv[3] if len(sys.argv) > 3 else None
T = tl['T']
DUR = tl['dur']
N = int(DUR * SR)
rng = np.random.default_rng(23)

music = np.zeros((N, 2))
sfx = np.zeros((N, 2))
dry = np.zeros((N, 2))


def tt(d):
    return np.arange(int(d * SR)) / SR


def fade(s, a=0.003, r=0.01):
    s = s.copy()
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    s[:na] *= np.linspace(0, 1, na)
    s[-nr:] *= np.linspace(1, 0, nr)
    return s


def bp(s, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), s)


def lp(s, f, order=2):
    return sosfilt(butter(order, f, btype='low', fs=SR, output='sos'), s)


def hp(s, f, order=2):
    return sosfilt(butter(order, f, btype='high', fs=SR, output='sos'), s)


def put(bus, sig, t0, gain=1.0, pan=0.0):
    i0 = int(round(t0 * SR))
    if i0 >= N:
        return
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4
        sig = np.stack([sig * np.cos(a) * 1.414, sig * np.sin(a) * 1.414], axis=1)
    if i0 < 0:
        sig, i0 = sig[-i0:], 0
    sig = sig[:N - i0]
    bus[i0:i0 + len(sig)] += sig * gain


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------- recipes ----------------
def ping(f1=1760, f2=2637):
    t = tt(0.9)
    s = np.sin(2 * np.pi * f1 * t) * np.exp(-t / 0.18) + 0.5 * np.sin(2 * np.pi * f2 * t) * np.exp(-t / 0.12)
    return fade(s, 0.002, 0.05)


def click(d=0.006, lo=2500, hi=9000):
    s = bp(rng.standard_normal(int(d * SR) + 400), lo, hi)[:int(d * SR)]
    return fade(s * np.exp(-tt(d) / (d / 3)), 0.0005, 0.002)


def thud(f0=150, tau=0.08):
    t = tt(0.4)
    f = f0 * (0.62 + 0.38 * np.exp(-t / 0.05))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau)
    return fade(s + hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.006) * 0.2, 0.001, 0.03)


def heartbeat():
    return thud(62, 0.12) * 1.0


def stamp():
    t = tt(0.5)
    s = lp(rng.standard_normal(len(t)), 900) * np.exp(-t / 0.05) * 1.2 + np.sin(2 * np.pi * 80 * t) * np.exp(-t / 0.12)
    return fade(s, 0.001, 0.05)


def whoosh(d=0.5, lo=500, hi=5000, rise=True):
    t = tt(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    seg = 1024
    for i in range(0, len(n), seg):
        x = i / len(n)
        x = x if rise else 1 - x
        fc = lo * (hi / lo) ** x
        out[i:i + seg] = bp(n[max(0, i - 2048):i + seg], fc * 0.7, min(fc * 1.4, 20000))[-len(n[i:i + seg]):]
    s = out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    pan = np.linspace(-0.6, 0.6, len(t))
    return np.stack([s * np.cos((pan + 1) * np.pi / 4), s * np.sin((pan + 1) * np.pi / 4)], axis=1) * 1.414


def tape_rewind(d=0.35):
    t = tt(d)
    f = 300 + 2600 * (t / d) ** 1.5
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25 + bp(rng.standard_normal(len(t)), 800, 6000) * 0.6
    return fade(lp(s, 5000) * (t / d) ** 0.7, 0.01, 0.02)


def ring_burst():
    t = tt(0.65)
    car = np.sin(2 * np.pi * 1300 * t) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 18 * t)))
    return fade(car * np.exp(-t / 0.8) * 0.6 + np.sin(2 * np.pi * 1600 * t) * (0.5 - 0.5 * np.sign(np.sin(2 * np.pi * 18 * t))) * 0.3, 0.004, 0.05)


def pop(f=700):
    t = tt(0.16)
    fr = f * (0.62 + 0.38 * np.exp(-t / 0.018))
    return fade(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.045), 0.001, 0.02)


def bonk():
    t = tt(0.35)
    f = 220 * (0.7 + 0.3 * np.exp(-t / 0.08))
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.09)
    return fade(lp(s, 1800) * 0.5, 0.002, 0.03)


def tick():
    t = tt(0.025)
    return fade(np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.003) + 0.4 * click(0.025, 4000, 12000), 0.0003, 0.004)


def tap():
    t = tt(0.03)
    return fade(bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.006), 0.0005, 0.005)


def pluck(f, d=0.45, tau=0.12):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05)) * np.exp(-t / tau)
    return fade(s, 0.002, 0.03)


def snapclick(f):
    s = pluck(f, 0.3, 0.06) * 0.8
    c = click(0.01, 3000, 10000)
    s[:len(c)] += c * 0.6
    return s


def bell(f, d=1.4, tau=0.5):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / 0.2)) * np.exp(-t / tau)
    return fade(s, 0.003, 0.1)


def kick():
    t = tt(0.35)
    f = 48 + 90 * np.exp(-t / 0.03)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14), 0.001, 0.03)


def clap():
    t = tt(0.25)
    env = np.zeros_like(t)
    for o in (0, 0.012, 0.024):
        env += (t >= o) * np.exp(-np.maximum(0, t - o) / 0.02)
    return fade(bp(rng.standard_normal(len(t)), 900, 5000) * env * 0.6, 0.001, 0.03)


def pad(midis, dur, seed, cutoff=1900):
    r = np.random.default_rng(seed)
    t = tt(dur)
    out = np.zeros((len(t), 2))
    for ch in range(2):
        s = np.zeros(len(t))
        for m in midis:
            for det in (-0.09, 0.0, 0.08):
                f = mtof(m) * 2 ** (det / 12)
                for h in range(1, 7):
                    s += np.sin(2 * np.pi * f * h * t + r.uniform(0, 2 * np.pi)) / h ** 1.6
        out[:, ch] = lp(s, cutoff)
    a, rl = min(0.6, dur / 3), min(0.7, dur / 3)
    env = np.minimum(1, t / a) * np.minimum(1, (dur - t) / rl)
    return out * env[:, None] / (len(midis) * 3)


def drone(d):
    t = tt(d)
    s = np.zeros(len(t))
    for m, g in ((33, 1.0), (40, 0.6), (45, 0.4), (46, 0.12)):
        for det in (-0.06, 0.05):
            f = mtof(m) * 2 ** (det / 12)
            s += g * (2 * ((f * t) % 1) - 1)
    cut = 180 + 2200 * (t / d) ** 2
    out = np.zeros_like(s)
    seg = 2048
    for i in range(0, len(s), seg):
        out[i:i + seg] = lp(s[max(0, i - 4096):i + seg], cut[min(i, len(cut) - 1)])[-len(s[i:i + seg]):]
    return out * (0.25 + 0.75 * (t / d) ** 1.5)


def sub(m, d, beat=0.5):
    t = tt(d)
    s = np.sin(2 * np.pi * mtof(m) * t)
    env = (1 - 0.8 * np.exp(-(t % beat) / 0.1)) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.1)
    return s * env


# ---------------- 0:00-0:03 hook ----------------
room = lp(rng.standard_normal(N), 500) * 0.004
put(dry, np.stack([room, np.roll(room, 997)], axis=1), 0)
put(sfx, ping(), 0.02, 0.45)
for i in range(5):
    put(sfx, click(0.008, 2000, 7000), T['h1'] + i * T['stag'], 0.12)
for i in range(6):
    put(sfx, click(0.008, 2000, 7000), T['h2'] + i * T['stag'], 0.12)
put(sfx, heartbeat(), T['hit'], 0.9)
put(sfx, heartbeat(), T['hit'] + 0.24, 0.6)
put(sfx, stamp(), T['stamp'], 0.5)

# ---------------- 0:03-0:12 the replay (tension) ----------------
put(sfx, tape_rewind(0.3), T['s2'] - 0.2, 0.25)
put(music, drone(T['amn'] - T['s2']), T['s2'], 0.05)
tk_t, iv = T['s2'] + 0.2, 0.5
while tk_t < T['amn']:
    put(sfx, tick(), tk_t, 0.12, pan=0.4)
    tk_t += iv
    iv = max(0.17, iv * 0.94)
cards = T['cards']
put(sfx, ping(1568, 2349), cards[0], 0.4, pan=-0.3)
put(sfx, ring_burst(), cards[1], 0.32, pan=0.3)
put(sfx, whoosh(0.35, 1200, 7000), cards[2] - 0.05, 0.3, pan=-0.2)
put(sfx, pop(900), cards[3], 0.35, pan=0.3)
put(sfx, pop(1200), cards[3] + 0.09, 0.3, pan=0.3)
put(sfx, bonk(), cards[4], 0.35)
for k, c in enumerate(cards):
    put(sfx, thud(110 - k * 6, 0.07), c, 0.35)
put(sfx, pluck(mtof(76), 0.6, 0.18), T['bigbub'], 0.25)
put(sfx, pluck(mtof(72), 0.8, 0.25), T['bigbub'] + 0.14, 0.25)
# the pile-up: more and more notifications, faster and faster
r2 = np.random.default_rng(5)
x = 5.6
while x < T['amn'] - 0.05:
    put(sfx, ping(r2.choice([1568, 1760, 1976, 2093]), r2.choice([2349, 2637, 3136])), x, 0.12 + 0.12 * (x - 5.6) / 4.6, pan=r2.uniform(-0.9, 0.9))
    x += max(0.09, 0.5 - (x - 5.6) * 0.1)
# hard cut to silence on "amnesia"
cut = int(T['amn'] * SR)
for bus in (music, sfx):
    bus[cut - 96:cut] *= np.linspace(1, 0, 96)[:, None]
    bus[cut:int((T['amn'] + 0.8) * SR)] = 0
put(sfx, thud(55, 0.2), T['cost'], 0.35)

# ---------------- 0:12-0:16 the snap ----------------
put(sfx, tape_rewind(0.35), T['rewind'], 0.3)
notes = [72, 74, 76, 79, 81]
for i, lt in enumerate(T['land']):
    put(sfx, whoosh(0.4, 900, 4500), lt - 0.42, 0.12, pan=-0.5 + 0.25 * i)
    put(sfx, snapclick(mtof(notes[i] + 12)), lt, 0.3, pan=-0.4 + 0.2 * i)
put(music, pad([48, 55, 60, 64, 67, 74], 3.4, 11, 2600), T['links'] - 0.05, 1.0)   # resolves: Cadd9
put(sfx, bell(mtof(84), 2.2, 0.8), T['logo'], 0.08)

# ---------------- 0:16-0:27 the replay, fixed (calm bed, clear for the AI voice) ----------------
bed = [(16.0, 3.0, [45, 52, 57, 60, 64, 71]), (19.0, 4.0, [41, 48, 53, 57, 60, 67]), (23.0, 4.1, [48, 55, 60, 64, 67, 74])]
for i, (st, du, v) in enumerate(bed):
    put(music, pad(v, du + 0.6, 20 + i, 1500), st - 0.2, 0.8)
for t0 in np.arange(T['typing'], T['fxB2'] - 0.05, 0.11):
    put(sfx, tap(), t0, 0.08, pan=0.3)
put(sfx, pop(1100), T['fxB2'], 0.25, pan=0.3)
put(sfx, pop(800), T['fxB3'], 0.2, pan=-0.3)
put(sfx, whoosh(0.4, 400, 2500), T['nextDay'], 0.1)
put(sfx, pluck(mtof(79), 0.5, 0.1), T['call'] + 0.1, 0.12)
put(sfx, pluck(mtof(86), 0.5, 0.1), T['call'] + 0.2, 0.12)
put(sfx, bell(mtof(88), 1.6, 0.6), T['memPill'], 0.07)
duck = np.ones(N)
a0, a1 = int((T['voice'] - 0.3) * SR), int((T['voiceEnd'] + 0.3) * SR)
duck[a0:a1] = 0.35
duck = np.convolve(duck, np.ones(4800) / 4800, mode='same')

# ---------------- 0:27-0:35 autopilot (upbeat) ----------------
beat = 0.5
prog = [(27.0, [41, 48, 53, 57, 64], 41), (29.0, [48, 55, 60, 64, 67], 48), (31.0, [43, 50, 55, 59, 62], 43), (33.0, [45, 52, 57, 60, 64], 45)]
for i, (st, v, b) in enumerate(prog):
    put(music, pad(v, 2.3, 40 + i, 2200), st - 0.05, 0.75)
    put(music, sub(b, 2.0), st, 0.16)
    arp = [v[2] + 12, v[3] + 12, v[4] + 12, v[3] + 12]
    for k in range(8):
        put(music, pluck(mtof(arp[k % 4])), st + k * 0.25, 0.07, pan=0.4 * np.sin(k * 1.3))
for k in range(16):
    tb = 27.0 + k * beat
    put(music, kick(), tb, 0.35)
    if k % 2 == 1:
        put(music, clap(), tb, 0.18, pan=0.1)
for a in T['ap']:
    put(sfx, snapclick(mtof(84)), a, 0.25)
    put(sfx, whoosh(0.3, 1500, 6000), a - 0.1, 0.1)
for t0 in np.arange(T['ap'][3] + 0.2, T['ap'][3] + 1.2, 0.07):
    put(sfx, tap(), t0, 0.07, pan=0.2)
for st_t in (T['stage1'], T['stage2']):
    put(sfx, whoosh(0.3, 800, 3500), st_t, 0.14)
    put(sfx, snapclick(mtof(88)), st_t + 0.3, 0.2)

# ---------------- 0:35-0:40 the mirror ----------------
put(music, pad([45, 52, 57, 60, 64, 71], 1.9, 60, 1700), 35.0, 0.6)
put(music, sub(45, 1.7, 0.5), 35.0, 0.12)
put(sfx, whoosh(0.4, 500, 3000), T['s6'], 0.18)
put(sfx, bonk(), T['s6'] + 0.5, 0.18, pan=-0.5)
put(sfx, snapclick(mtof(84)), T['s6'] + 0.6, 0.18, pan=0.5)
stop0, stop1 = int(T['stop'] * SR), int(T['m2'] * SR)
music[stop0:stop1] *= 0.0
put(music, kick(), T['m2'], 0.45)
put(music, pad([48, 55, 60, 64, 67, 74], 3.1, 61, 2000), T['m2'], 0.75)
put(music, sub(48, 3.0, 0.5), T['m2'], 0.12)

# ---------------- 0:40-0:45 offer + loop ----------------
put(music, pad([41, 48, 53, 57, 60, 67], 2.6, 70, 1600), 40.0, 0.7)
put(music, pad([48, 55, 60, 64, 67, 74], 2.9, 71, 1500), 42.3, 0.6)
for k in range(5):
    put(music, thud(60, 0.15), 40.2 + k * 1.0, 0.25)
put(sfx, pop(560), T['cta'] + 0.02, 0.3)
put(sfx, bell(mtof(91), 1.2, 0.4), T['cta'] + 0.05, 0.07)
for k in range(2):
    put(sfx, bell(mtof(96), 0.8, 0.2), T['cta'] + 0.6 + k * 1.6, 0.04)
tail = np.ones(N)
l0 = int((T['loop'] - 0.1) * SR)
tail[l0:] = np.linspace(1, 0, N - l0) ** 1.5
music *= tail[:, None]
sfx *= tail[:, None]


# ---------------- reverb + master ----------------
def reverb_ir(t60=1.8, seed=5):
    r = np.random.default_rng(seed)
    t = tt(t60)
    env = np.exp(-6.91 * t / t60)
    ir = np.stack([lp(r.standard_normal(len(t)), 6000) * env, lp(r.standard_normal(len(t)), 6000) * env], axis=1)
    ir[:int(0.012 * SR)] = 0
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


ir = reverb_ir()


def verb(x, wet):
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:N] for c in range(2)], axis=1)
    return x + wet * y


mix = (verb(music, 0.25) * 0.9 * duck[:, None]) + verb(sfx, 0.12) + dry
# keep the silence after "amnesia" truly silent (reverb tails included)
mix[cut:int((T['amn'] + 0.75) * SR)] *= 0.02
if VOICE:
    vsr, v = wavfile.read(VOICE)
    v = v.astype(np.float64)
    v = v.mean(axis=1) if v.ndim > 1 else v
    put(mix, v / (np.max(np.abs(v)) + 1e-9) * 0.7, T['voice'], 1.0)
peak = np.max(np.abs(mix))
mix = np.tanh(mix / peak * 1.1) / np.tanh(1.1) * 0.89
wavfile.write(OUT, SR, mix.astype(np.float32))
print(f'wrote {OUT}: {DUR}s, AI voice slot {T["voice"]}-{T["voiceEnd"]}s {"filled" if VOICE else "left clear"}')
