# Highvance study-abroad ad

Motion graphic ad for study-abroad consultancies: hook, pain point, a real AI call, the "8 SECONDS" stat, then the CTA.
The call is a real recording of Aarushi (the AI agent) calling Sumit about a Germany enquiry, in Hinglish.

## Files in `exports/`

| File | What it is |
|---|---|
| `highvance-study-abroad-ad-9x16.mp4` | The ad: 1080 × 1920, 30 fps, about 56 s, with a 32-second cut of the call |
| `highvance-study-abroad-ad-1x1.mp4` | The same ad laid out for feed, 1080 × 1080 |
| `highvance-study-abroad-full-call-9x16.mp4` | The whole 2:40 call in the same design (about 3:05), for a landing page, YouTube or sales follow-ups |
| `highvance-study-abroad-music-sfx.wav` | The ad's music and sound effects without the call, 48 kHz 24-bit |
| `call-audio-ad-cut.wav` | The edited call on its own, levelled to -16 LUFS |
| `captions-ad.srt`, `captions-full.srt` | The call transcript with timings, in video time |
| `storyboard-9x16.png` | Key frames of the ad, for review |

## The call

- `call/transcript.json` holds the transcript (Roman-script Hinglish, split into caption lines), the speaker turns, the
  ad cut's edit list and the capability tags. `call/transcript.md` is the same transcript as a table to proofread.
- The ad cut keeps the call in order and cuts only at pauses. It runs from the greeting to Aarushi offering the free video call with Priya.
- The tags follow what happens in the call: Instant Callback, Eligibility Check, IELTS Checked, Free Counselling Offered
  (and, in the full version, Universities Suggested, Admission Process Explained, Fees & Living Costs Answered).

## Rebuilding

`CALL_AUDIO=/path/to/Audio_Study_abroad.m4a ./build.sh`

`make_call.py` cleans and levels the recording, applies the cut, times every caption word to the speech and writes
`call-data-<cut>.js`. `meera-ad.html` holds the animation (open it in a browser to preview; add `?cut=full` or `?fmt=s`).
`render.mjs` renders the frames, `sound.py` builds the music and effects around the call, and `srt.py` writes the captions.
To fix a caption, edit its line in `call/transcript.json` and rebuild. To change the ad cut, edit `cuts.ad` there.

The music and sound effects are synthesized in `sound.py`, so there is nothing to license.
