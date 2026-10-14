"""Sound design for the Highvance study-abroad ad.

Builds the music + SFX bed from the timeline the animation exports, so every hit lands
on its frame. The call slot (from 0:14 for the length of the recording) stays clear of
music; pass the processed call audio to get the full mix as well.

    python3 sound.py timeline_v.json bed.wav [call.wav full_mix.wav]
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
tl = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
CALL = sys.argv[3] if len(sys.argv) > 4 else None
FULL = sys.argv[4] if len(sys.argv) > 4 else None
T = tl['T']
DUR = tl['dur']
N = int(DUR * SR)
rng = np.random.default_rng(11)

music = np.zeros((N, 2))
sfx = np.zeros((N, 2))
dry = np.zeros((N, 2))  # sounds that skip the reverb (ringback, phone tones)


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


# ---------------- sound recipes ----------------
def ping():
    t = tt(1.0)
    s = (np.sin(2 * np.pi * 1760 * t) * np.exp(-t / 0.20)
         + 0.55 * np.sin(2 * np.pi * 2637 * t) * np.exp(-t / 0.13)
         + 0.18 * np.sin(2 * np.pi * 5274 * t) * np.exp(-t / 0.03))
    return fade(s, 0.002, 0.05)


def marimba(f, d=0.6):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.26)
         + 0.32 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.045)
         + 0.10 * np.sin(2 * np.pi * 9.9 * f * t) * np.exp(-t / 0.012))
    return fade(s, 0.002, 0.05)


def click(d=0.006, lo=2500, hi=9000):
    s = bp(rng.standard_normal(int(d * SR) + 400), lo, hi)[:int(d * SR)]
    return fade(s * np.exp(-tt(d) / (d / 3)), 0.0005, 0.002)


def riser(d):
    t = tt(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    seg = 1024
    for i in range(0, len(n), seg):
        x = i / len(n)
        fc = 400 + 7000 * x ** 2
        out[i:i + seg] = bp(n[max(0, i - 2048):i + seg], fc * 0.6, min(fc * 1.6, 20000))[-len(n[i:i + seg]):]
    env = (t / d) ** 2.2
    return fade(out * env, 0.05, 0.01)


def impact(big=1.0):
    t = tt(2.2)
    f = 38 + 85 * np.exp(-t / 0.09)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.42 * big))
    body = lp(rng.standard_normal(len(t)), 380) * np.exp(-t / 0.10) * 1.4
    snap = hp(rng.standard_normal(len(t)), 3500) * np.exp(-t / 0.008) * 0.5
    return fade(sub * 1.0 + body + snap, 0.0008, 0.3)


def thud(f0=150):
    t = tt(0.35)
    f = f0 * (0.62 + 0.38 * np.exp(-t / 0.05))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
    s += hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.006) * 0.25
    return fade(s, 0.001, 0.03)


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
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    s = out * env
    pan = np.linspace(-0.6, 0.6, len(t))
    return np.stack([s * np.cos((pan + 1) * np.pi / 4), s * np.sin((pan + 1) * np.pi / 4)], axis=1) * 1.414


def pop(f=700):
    t = tt(0.16)
    fr = f * (0.62 + 0.38 * np.exp(-t / 0.018))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.045)
    return fade(s, 0.001, 0.02)


def tick():
    t = tt(0.025)
    s = np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.003) + 0.4 * click(0.025, 4000, 12000)
    return fade(s, 0.0003, 0.004)


def flick():
    t = tt(0.12)
    s = bp(rng.standard_normal(len(t)), 1800, 7000) * (np.exp(-t / 0.03) * (1 - np.exp(-t / 0.004)))
    return fade(s, 0.001, 0.01)


def bell(f, d=1.4, tau=0.5):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / 0.2)) * np.exp(-t / tau)
    return fade(s, 0.003, 0.1)


def ringback(d):
    t = tt(d)
    s = np.sin(2 * np.pi * 400 * t) * np.sin(2 * np.pi * 25 * t)
    return fade(s, 0.012, 0.012)


def tone(f, d):
    return fade(np.sin(2 * np.pi * f * tt(d)), 0.005, 0.015)


def swell(d=0.9):
    t = tt(d)
    s = lp(rng.standard_normal(len(t)), 1800) * (t / d) ** 2.5
    return fade(s, 0.01, 0.06)


# ---------------- music ----------------
def pad(midis, dur, seed):
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
        out[:, ch] = lp(s, 1900)
    a, rl = min(0.5, dur / 3), min(0.6, dur / 3)
    env = np.minimum(1, t / a) * np.minimum(1, (dur - t) / rl)
    return out * env[:, None] / (len(midis) * 3)


def pluck(f, d=0.4):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05)) * np.exp(-t / 0.11)
    return fade(s, 0.002, 0.03)


def sub_bass(m, dur, beat=0.5, pump=True):
    t = tt(dur)
    s = np.sin(2 * np.pi * mtof(m) * t) + 0.18 * np.sin(2 * np.pi * 2 * mtof(m) * t)
    env = 1 - 0.75 * np.exp(-(t % beat) / 0.11) if pump else np.ones_like(t)
    env *= np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.12)
    return s * env


HOOK = [  # (start, dur, pad voicing, bass, arp tones)
    (0.00, 2.0, [57, 60, 64, 67, 71], 45, [69, 72, 76, 79]),   # Am9
    (2.00, 2.0, [53, 57, 60, 64, 67], 41, [65, 69, 72, 76]),   # Fmaj9
    (4.00, 2.0, [48, 55, 60, 64, 74], 48, [67, 72, 74, 76]),   # Cadd9
    (6.00, 2.0, [55, 59, 62, 64, 69], 43, [67, 71, 74, 76]),   # G6/9
    (8.00, 1.6, [57, 60, 64, 67, 71], 45, [69, 72, 76, 79]),   # Am9 (fades under the wipe)
]
for i, (st, du, v, b, arp) in enumerate(HOOK):
    put(music, pad(v, du + 0.5, 100 + i), st - 0.05, 0.9)
    put(music, sub_bass(b, du + 0.02), st, 0.16)
    k = 0
    a = st
    while a < st + du - 0.01:
        f = mtof(arp[k % len(arp)] + (12 if (k // 4) % 2 else 0))
        put(music, pluck(f), a, 0.10, pan=0.35 * np.sin(k * 1.3))
        a += 0.25
        k += 1
# fade the hook music out through the wipe into the call
hook_env = np.ones(N)
f0, f1 = int(8.55 * SR), int(9.6 * SR)
hook_env[f0:f1] = np.linspace(1, 0, f1 - f0) ** 1.5
hook_env[f1:] = 0

CLOSE = [
    (T['iris'] + 0.45, 2.10, [53, 57, 60, 64, 67], 41, [65, 69, 72, 76]),   # Fmaj9
    (T['iris'] + 2.55, 2.70, [48, 55, 60, 64, 74], 48, [67, 72, 74, 79]),   # Cadd9, resolves
]
close = np.zeros((N, 2))
for i, (st, du, v, b, arp) in enumerate(CLOSE):
    put(close, pad(v, du + 0.6, 200 + i), st - 0.1, 0.95)
    put(close, sub_bass(b, du, pump=False), st, 0.10)
    a, k = st + 0.25, 0
    while a < st + du - 0.1:
        put(close, pluck(mtof(arp[k % len(arp)] + 12)), a, 0.06, pan=0.4 * np.sin(k * 1.7))
        a += 0.5
        k += 1
close_env = np.zeros(N)
c0, c1, c2 = int((T['iris'] + 0.30) * SR), int((T['iris'] + 1.0) * SR), int((DUR - 0.65) * SR)
close_env[c0:c1] = np.linspace(0, 1, c1 - c0)
close_env[c1:c2] = 1
close_env[c2:] = np.linspace(1, 0, N - c2) ** 1.3
music = music * hook_env[:, None] + close * close_env[:, None]

# ---------------- SFX on the timeline ----------------
# hook
put(sfx, ping(), 0.03, 0.55)
ring_notes = [81, 84, 88, 93, 88, 84]
for b0, b1 in tl['ringtone']:
    for k, m in enumerate(ring_notes):
        tk = b0 + k * 0.16
        if tk < b1 - 0.05:
            put(sfx, marimba(mtof(m)), tk, 0.22, pan=-0.2 + 0.08 * k)
for tw in tl['hookWords']:
    put(sfx, click(0.008, 2000, 7000), tw, 0.10)
put(sfx, riser(0.55), T['lakh'] - 0.55, 0.20)
put(sfx, impact(1.0), T['lakh'], 0.75)
for k, tw in enumerate(tl['weekWords']):
    put(sfx, thud(150 - k * 8), tw, 0.45)
put(sfx, whoosh(0.32, 1500, 7000), T['bar'] - 0.08, 0.10)
put(sfx, whoosh(0.45, 600, 4000), T['l3'] - 0.1, 0.16)
# cut the ringtone hard at the scene change
cut = int(T['pain'] * SR)
sfx[cut - 120:cut] *= np.linspace(1, 0, 120)[:, None]
sfx[cut:cut + int(0.9 * SR)] = 0

# pain point
put(sfx, thud(95), T['pain'], 0.55)
freeze = tl['spawns'][-1]
for k, ts in enumerate(tl['spawns']):
    g = 0.30 * (0.55 + 0.45 * np.exp(-k / 10))
    put(sfx, pop(620 + 140 * ((k * 5) % 7) / 6), ts, g, pan=-0.45)
tk, iv = 4.15, 0.26
while tk < freeze:
    put(sfx, tick(), tk, 0.12, pan=0.5)
    tk += iv
    iv = max(0.045, iv * 0.93)
for ft in tl['flips']:
    put(sfx, flick(), ft, 0.30, pan=0.5)
put(sfx, bell(mtof(88), 1.2, 0.35), T['pick'], 0.14)
put(sfx, bell(mtof(93), 1.4, 0.45), T['pick'] + 0.09, 0.12)
put(sfx, whoosh(0.6, 300, 6000), T['wipeA'] - 0.05, 0.38)

# demo intro: pill, ringback, connect
put(sfx, pop(980), T['live'], 0.16)
for b0, b1 in tl['ringback']:
    put(dry, ringback(b1 - b0), b0, 0.24)
# low tension drone under the demo intro; gone before the call connects
dt = tt(4.9)
drone = (np.sin(2 * np.pi * mtof(33) * dt) + 0.5 * np.sin(2 * np.pi * mtof(40) * dt + 1.0)
         + 0.25 * np.sin(2 * np.pi * mtof(45) * dt * 1.002)) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.6 * dt))
drone += lp(rng.standard_normal(len(dt)), 900) * 0.18
denv = np.minimum(1, dt / 0.9) * np.clip((4.9 - dt) / 0.45, 0, 1)
put(music, drone * denv, 9.1, 0.07)
put(dry, tone(1046.5, 0.07), T['connect'] - 0.30, 0.10)
put(dry, tone(1568.0, 0.10), T['connect'] - 0.22, 0.10)
# from T['connect'] the call recording plays; no music or effects under it

# stat: count-up ticks, slam, then silence
roll, slam = T['roll'], T['slam']
for k in range(1, 9):
    p = 1 - (1 - k / 8) ** (1 / 3)
    put(sfx, tick(), roll + p * (slam - roll) - 0.01, 0.16)
put(sfx, impact(1.4), slam, 0.95)

# CTA
put(sfx, swell(0.75), T['iris'] - 0.05, 0.10)
put(sfx, bell(mtof(84), 1.6, 0.6), T['ctaLogo'], 0.07)
put(sfx, pop(560), T['btn'] + 0.02, 0.24)
put(sfx, bell(mtof(91), 1.2, 0.4), T['btn'] + 0.04, 0.06)


# ---------------- reverb + master ----------------
def reverb_ir(t60=2.0, seed=5):
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


mix = verb(music, 0.28) * 0.9 + verb(sfx, 0.14) + dry
# keep the call slot clean (tails from 13.9 decay naturally, nothing new enters)
peak = np.max(np.abs(mix))
mix = np.tanh(mix / peak * 1.1) / np.tanh(1.1) * 0.89
wavfile.write(OUT, SR, mix.astype(np.float32))
print(f'wrote {OUT}: {DUR:.2f}s, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS')

if CALL:
    csr, call = wavfile.read(CALL)
    assert csr == SR, 'call audio must be 48 kHz'
    call = call.astype(np.float64)
    if call.ndim > 1:
        call = call.mean(axis=1)
    full = mix.copy()
    put(full, call, T['connect'], 1.0)
    pk = np.max(np.abs(full))
    if pk > 0.97:
        full = np.tanh(full / pk * 1.2) / np.tanh(1.2) * 0.95
    wavfile.write(FULL, SR, full.astype(np.float32))
    print(f'wrote {FULL} with the call at {T["connect"]:.2f}s ({len(call) / SR:.2f}s)')
