"""Prepares the real call recording for the ad.

Reads the recording, the curated transcript (call/transcript.json) and an edit list, then
writes the processed call audio (48 kHz, cleaned, levelled to -16 LUFS) and call-data-<cut>.js,
which the animation uses for captions, speaker turns, the orb's loudness and tag timings.

    python3 make_call.py <recording> call/transcript.json <cut: full|ad> <out.wav> <out.js>
"""
import json
import re
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
src, tr_path, cut, out_wav, out_js = sys.argv[1:6]
tr = json.load(open(tr_path))

# ---------- load + clean ----------
raw = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
x = sosfilt(butter(2, 85, btype='high', fs=SR, output='sos'), x)

utts = tr['utterances']


def spans(sp):
    return [(u['a'], u['b']) for u in utts if u['sp'] == sp]


def rms(sp):
    v = np.concatenate([x[int(a * SR):int(b * SR)] for a, b in spans(sp)])
    return np.sqrt(np.mean(v ** 2))


# bring the student's voice level up to the agent's (phone recordings are often uneven)
diff_db = 20 * np.log10(rms('a') / rms('s'))
boost = 10 ** (np.clip(diff_db, 0, 6) / 20)
g = np.ones_like(x)
ramp = int(0.03 * SR)
for a, b in spans('s'):
    i0, i1 = int(max(0, a - 0.05) * SR), int(min(len(x) / SR, b + 0.05) * SR)
    g[i0:i1] = boost
    g[max(0, i0 - ramp):i0] = np.linspace(1, boost, i0 - max(0, i0 - ramp))
    g[i1:i1 + ramp] = np.linspace(boost, 1, len(g[i1:i1 + ramp]))
x = x * g

# ---------- edit ----------
if cut == 'full':
    last = max(u['b'] for u in utts)
    ranges = [[0.0, min(len(x) / SR, last + 0.35)]]
else:
    ranges = tr['cuts'][cut]
xf = int(0.012 * SR)
pieces, out_off = [], []
pos = 0.0
for a, b in ranges:
    seg = x[int(a * SR):int(b * SR)].copy()
    seg[:xf] *= np.linspace(0, 1, xf)
    seg[-xf:] *= np.linspace(1, 0, xf)
    pieces.append(seg)
    out_off.append(pos)
    pos += len(seg) / SR
y = np.concatenate(pieces)
DUR = len(y) / SR


def to_out(t):
    for (a, b), o in zip(ranges, out_off):
        if a - 1e-6 <= t <= b + 1e-6:
            return o + (t - a)
    return None


# ---------- loudness: -16 LUFS, true peak under -1.5 dB ----------
tmp = out_wav + '.tmp.wav'
wavfile.write(tmp, SR, y.astype(np.float32))
meas = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                      capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp, '-af',
                f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", '-ar', str(SR), '-c:a', 'pcm_f32le', out_wav], check=True)
subprocess.run(['rm', '-f', tmp])
_, y = wavfile.read(out_wav)
y = y.astype(np.float64)

# ---------- word timings ----------
# speech islands (pauses >= 0.2 s split them) from the fine VAD pass, in source time
islands = tr['islands']


def syllables(w):
    w = w.lower()
    if re.search(r'\d', w):
        return 2 + 1.2 * len(re.sub(r'\D', '', w))
    return max(1, len(re.findall(r'[aeiouy]+', w)))


chunks = []
for ui, u in enumerate(utts):
    if not u['text'].strip() or to_out(u['a']) is None or to_out(u['b']) is None:
        continue
    isl = [[max(a, u['a']), min(b, u['b'])] for a, b in islands if b > u['a'] and a < u['b']]
    isl = [s for s in isl if s[1] - s[0] > 0.05] or [[u['a'], u['b']]]
    phrases = [p.strip() for p in u['text'].split('|') if p.strip()]
    words = [w for p in phrases for w in p.split()]
    weights = np.array([syllables(w.strip('*')) for w in words], float)
    speech = sum(b - a for a, b in isl)
    cum = np.concatenate([[0], np.cumsum(weights)]) / weights.sum() * speech

    def at(d):  # speech-time offset -> source time, skipping pauses
        for a, b in isl:
            if d <= b - a + 1e-9:
                return a + d
            d -= b - a
        return isl[-1][1]

    wi = 0
    for p in phrases:
        ws = []
        for w in p.split():
            a, b = at(cum[wi]), at(cum[wi + 1])
            kw = w.startswith('*') and w.endswith('*')
            ws.append({'w': w.strip('*'), 'a': round(to_out(a), 3), 'b': round(to_out(b), 3), 'kw': kw})
            wi += 1
        chunks.append({'sp': u['sp'], 'words': ws})

# ---------- loudness envelope for the orb, 50 per second ----------
RATE = 50
hop = SR // RATE
n = len(y) // hop
db = np.array([20 * np.log10(np.sqrt(np.mean(y[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(n)])
lo, hi = np.percentile(db, 25), np.percentile(db, 99)
env = np.clip((db - lo) / (hi - lo), 0, 1) ** 1.3
spk = ['-'] * n
for u in utts:
    oa, ob = to_out(u['a']), to_out(u['b'])
    if oa is None or ob is None:
        continue
    for i in range(int(oa * RATE), min(n, int(ob * RATE) + 1)):
        spk[i] = u['sp']

# ---------- capability tags ----------
# anchored in source time; if an anchor falls inside a removed part, it moves to the next kept moment
tags = []
for tg in tr['tags']:
    if cut not in tg.get('cuts', ['full', 'ad']):
        continue
    t = to_out(tg['src'])
    if t is None:
        later = [o for (a, b), o in zip(ranges, out_off) if a > tg['src']]
        t = later[0] if later else DUR - 1.0
    tags.append({'txt': tg['txt'], 't': round(t, 3)})

data = {
    'cut': cut, 'dur': round(DUR, 3), 'agent': tr['agent'], 'lead': tr['lead'],
    'envRate': RATE, 'env': [round(float(v), 3) for v in env], 'spk': ''.join(spk),
    'chunks': chunks, 'tags': tags,
}
with open(out_js, 'w') as f:
    f.write('// generated by make_call.py from the real call recording\nwindow.CALL_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n')
print(f'{cut}: {DUR:.2f}s, {len(chunks)} caption lines, {sum(len(c["words"]) for c in chunks)} words, student boost {20 * np.log10(boost):.1f} dB')
