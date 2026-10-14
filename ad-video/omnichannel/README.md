# Highvance — "Your business has amnesia" (45 s Reel)

One customer, Ananya, reaches a business on four channels, repeats herself four times and buys elsewhere.
The same 48 hours replay with Highvance's one AI brain: instant reply, a call that remembers last night's chat,
automatic follow-up, analytics and CRM sync. It ends on "Are you A or B?" and "Comment AUDIT", and loops back to frame 1.
The script and post package are in `prompt.md`.

## Files in `exports/`

| File | What it is |
|---|---|
| `highvance-amnesia-9x16.mp4` | 1080 × 1920, 30 fps, 45 s, -14 LUFS, for Reels |
| `highvance-amnesia-1x1.mp4` | 1080 × 1080 feed version, re-laid out (not a crop) |
| `highvance-amnesia-music-sfx.wav` | Music and effects, 48 kHz 24-bit |
| `storyboard-9x16.png` | Key frames for review |

## The AI voice line

0:19.5–0:25.0 is left clear (music ducked) for the real product recording of:
"Hi Ananya! Kal raat aapne WhatsApp pe premium plan ke baare mein poocha tha — wahin se continue karein?"
The captions and orb are timed to an estimated pace. Record the line from the product, then run
`VOICE=/path/to/line.wav ./build.sh` (and re-time `AI_LINE` in `amnesia.html` if the recording runs longer than 5.5 s).

## Rebuilding

`./build.sh` renders both formats with headless Chromium (`render.mjs`), synthesizes the sound (`sound.py`, nothing to
license) and encodes the MP4s. Open `amnesia.html` in a browser to preview it live (`?fmt=s` for square).
