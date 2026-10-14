#!/usr/bin/env bash
# Rebuilds "Your business has amnesia": frames -> sound -> MP4s (9:16 and 1:1).
# Needs node with Playwright, python3 with numpy + scipy, and ffmpeg.
# VOICE=/path/to/ai-line.wav fills the AI voice slot (0:19.5-0:25) with the real product recording.
# SKIP_FRAMES=1 reuses frames already rendered in $WORK.
set -euo pipefail
cd "$(dirname "$0")"
WORK=${WORK:-/tmp/highvance-amnesia}
OUT=exports
mkdir -p "$WORK" "$OUT"
for F in v s; do
  [ "${SKIP_FRAMES:-0}" = 1 ] || { rm -rf "$WORK/$F"; node render.mjs $F "$WORK/$F"; }
done
python3 sound.py "$WORK/v/timeline_v.json" "$WORK/mix_raw.wav" ${VOICE:-}
# Instagram plays Reels at about -14 LUFS
ffmpeg -hide_banner -nostats -i "$WORK/mix_raw.wav" -af loudnorm=I=-14:TP=-1.5:LRA=20:print_format=json -f null - 2>"$WORK/ln.txt"
python3 - "$WORK" <<'PY'
import json, sys, re, subprocess
w = sys.argv[1]; t = open(w + '/ln.txt').read(); m = json.loads(t[t.rindex('{'):t.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', w + '/mix_raw.wav', '-af', af, '-ar', '48000', '-c:a', 'pcm_s24le', 'exports/highvance-amnesia-music-sfx.wav'], check=True)
PY
for F in v s; do
  NAME=$([ $F = v ] && echo 9x16 || echo 1x1)
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$WORK/$F/f%05d.jpg" -i "$OUT/highvance-amnesia-music-sfx.wav" \
    -vf "scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=full:out_range=tv,format=yuv420p" \
    -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$OUT/highvance-amnesia-$NAME.mp4"
done
ls -la "$OUT"
