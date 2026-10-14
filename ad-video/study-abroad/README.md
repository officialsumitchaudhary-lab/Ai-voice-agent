# Highvance study-abroad ad (54 s)

Motion graphic ad for study-abroad consultancies: hook, pain point, Meera's live call, the "8 SECONDS" stat, then the CTA.

## Files in `exports/`

| File | What it is |
|---|---|
| `highvance-study-abroad-ad-9x16.mp4` | 1080 × 1920, 30 fps, for Reels and Stories |
| `highvance-study-abroad-ad-1x1.mp4` | 1080 × 1080, re-laid out for feed (not a crop) |
| `highvance-study-abroad-music-sfx.wav` | 48 kHz 24-bit music and sound effects, without the call |
| `call-captions-timing.srt` | Where each caption line lands, to line up the real call recording |
| `storyboard-9x16.png` | Key frames, for review |

## The call slot

0:14.0 to 0:44.0 is left silent for the real Meera call recording (30.0 s). Place it on its own track starting at 0:14.0. The on-screen captions, the orb and the capability tags are timed to an estimated speaking pace, so they need re-timing to the real recording before the ad goes live.

## Rebuilding

`meera-ad.html` holds the whole animation; every frame is a function of time. Open it in a browser to preview (space pauses, arrow keys seek), or add `?fmt=s` for the square version. `./build.sh` renders the frames with headless Chromium, synthesizes the sound with `sound.py`, and encodes both MP4s. Edit the `CALL` segments in `meera-ad.html` to change the caption text or timings.

The music and sound effects are synthesized in `sound.py`, so there is nothing to license.
