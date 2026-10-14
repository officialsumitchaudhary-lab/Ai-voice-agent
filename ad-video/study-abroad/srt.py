"""Writes the call transcript as SRT, in video time, from the timeline the animation exports."""
import json
import sys

tl = json.load(open(sys.argv[1]))
chunks, toks = tl['chunks'], tl['tokens']
ends = {}
for c_i, c in enumerate(chunks):
    nxt = chunks[c_i + 1]['start'] if c_i + 1 < len(chunks) else tl['T']['stat'] - 0.3
    spoken = [t['b'] for t in toks if t['a'] >= c['start'] - 0.01 and t['b'] <= nxt + 0.01]
    ends[c_i] = min(nxt, max(spoken) + 0.35) if spoken else nxt


def ts(x):
    ms = int(round(x * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


with open(sys.argv[2], 'w') as f:
    for i, c in enumerate(chunks):
        who = f"{tl['agent']} (AI)" if c['sp'] == 'm' else 'Student'
        f.write(f"{i + 1}\n{ts(max(0, c['start']))} --> {ts(ends[i])}\n{who}: {c['text']}\n\n")
print('wrote', sys.argv[2])
