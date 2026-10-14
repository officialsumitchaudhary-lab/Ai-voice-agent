#!/usr/bin/env bash
# Rebuilds the Highvance study-abroad ad: frames -> sound -> MP4s.
# Needs node with Playwright, python3 with numpy + scipy, and ffmpeg.
# SKIP_FRAMES=1 reuses frames already in $WORK.
set -euo pipefail
cd "$(dirname "$0")"
WORK=${WORK:-/tmp/highvance-ad}
OUT=exports
mkdir -p "$WORK" "$OUT"

if [ "${SKIP_FRAMES:-0}" != 1 ]; then
  rm -rf "$WORK/fv" "$WORK/fs"
  node render.mjs v "$WORK/fv"
  node render.mjs s "$WORK/fs"
fi

python3 sound.py "$WORK/fv/timeline_v.json" "$WORK/mix_raw.wav"
ffmpeg -hide_banner -loglevel error -y -i "$WORK/mix_raw.wav" -af volume=-0.5dB -c:a pcm_s24le -ar 48000 "$OUT/highvance-study-abroad-music-sfx.wav"
python3 srt.py "$WORK/fv/timeline_v.json" "$OUT/call-captions-timing.srt"

for F in v s; do
  NAME=$([ "$F" = v ] && echo 9x16 || echo 1x1)
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$WORK/f$F/f%05d.jpg" -i "$OUT/highvance-study-abroad-music-sfx.wav" \
    -vf "scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=full:out_range=tv,format=yuv420p" \
    -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$OUT/highvance-study-abroad-ad-$NAME.mp4"
done
ls -la "$OUT"
