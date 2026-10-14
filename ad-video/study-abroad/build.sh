#!/usr/bin/env bash
# Rebuilds the Highvance study-abroad ad from the real call recording:
#   call audio + data -> frames -> sound -> MP4s, for the 30-second ad cut and the full call.
# Needs node with Playwright, python3 with numpy + scipy, and ffmpeg.
#   CALL_AUDIO=/path/to/Audio_Study_abroad.m4a ./build.sh
# SKIP_FRAMES=1 reuses frames already rendered in $WORK.
set -euo pipefail
cd "$(dirname "$0")"
: "${CALL_AUDIO:?set CALL_AUDIO to the call recording}"
WORK=${WORK:-/tmp/highvance-ad}
OUT=exports
mkdir -p "$WORK" "$OUT"

encode() { # frames-dir audio out
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f%05d.jpg" -i "$2" \
    -vf "scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=full:out_range=tv,format=yuv420p" \
    -c:v libx264 -preset slow -crf "${CRF:-17}" -profile:v high -level 4.2 -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$3"
}

for CUT in ad full; do
  python3 make_call.py "$CALL_AUDIO" call/transcript.json $CUT "$WORK/call-$CUT.wav" call-data-$CUT.js
  FMTS=$([ $CUT = ad ] && echo "v s" || echo "v")
  for F in $FMTS; do
    [ "${SKIP_FRAMES:-0}" = 1 ] || { rm -rf "$WORK/$CUT-$F"; node render.mjs $F "$WORK/$CUT-$F" --cut $CUT; }
  done
  python3 sound.py "$WORK/$CUT-v/timeline_v.json" "$WORK/bed-$CUT.wav" "$WORK/call-$CUT.wav" "$WORK/mix-$CUT.wav"
  python3 srt.py "$WORK/$CUT-v/timeline_v.json" "$OUT/captions-$CUT.srt"
  for F in $FMTS; do
    NAME=$([ $F = v ] && echo 9x16 || echo 1x1)
    LABEL=$([ $CUT = ad ] && echo ad || echo full-call)
    CRF=$([ $CUT = ad ] && echo 17 || echo 20) encode "$WORK/$CUT-$F" "$WORK/mix-$CUT.wav" "$OUT/highvance-study-abroad-$LABEL-$NAME.mp4"
  done
done
# stems for the editor: the ad's music + effects bed, and the edited call on its own
ffmpeg -hide_banner -loglevel error -y -i "$WORK/bed-ad.wav" -c:a pcm_s24le "$OUT/highvance-study-abroad-music-sfx.wav"
ffmpeg -hide_banner -loglevel error -y -i "$WORK/call-ad.wav" -c:a pcm_s24le "$OUT/call-audio-ad-cut.wav"
ls -la "$OUT"
