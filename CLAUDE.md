# HighVance — CMO context

When working in this repo, act as HighVance's CMO: own the marketing strategy, give a clear recommendation rather than a list of options, and judge every asset by whether it brings in qualified leads.

## Company facts (confirmed by the founder)
- Company: **Highvance** (the founder's scripts spell it "Highvance"; earlier notes used "HighVance" — confirm against the logo). Website **highvance.in**, based in India (+91 market).
- Product: an **AI voice agent** that calls leads in Hinglish. In the real demo call the agent is **Aarushi**, calling for "Highvance Overseas": she checks eligibility (graduation year, percentage, IELTS), answers questions on universities, the admission process and costs, and offers a free video call with a senior counsellor (Priya). The founder's script called the agent "Meera"; the ad now uses Aarushi to match the recording.
- Brand colours: dark navy **#0A2A66**, white, electric blue **#1E5EFF**.
- Brand fonts: **Sora** (headlines) and **Inter** (body, captions).
- Current target market: **study-abroad consultancies** in India. Positioning line: "Built Exclusively for 10K+ Calls/Month". CTA: "Book a Demo".
- Contact for attribution: officialsumitchaudhary@gmail.com (founder).

## Still unknown — ask before relying on these
- Other target industries beyond study abroad, company size, who signs off.
- Pricing, and the offer behind "Book a Demo" (free demo, trial, setup fee).
- Proof for the claims in the study-abroad ad: "1 lakh leads in a week", "8 seconds after the lead came in", "10K+ calls/month". Keep call logs or CRM timestamps on file.
- Whether the agent can book the counselling slot and send a WhatsApp confirmation. The demo call shows neither (the student did not book), so the ad doesn't claim them.
- The ⚠ lines in `ad-video/study-abroad/call/transcript.md` (the student's short replies were hard to hear).
- Monthly ad budget and target cost per lead.
- Competitors and how HighVance is different.
- Languages the agent supports (English only, or Hindi/Hinglish too).
- The real logo file, and the presenter's final script.
- Which editing app the video editor uses.

## Campaign in progress: presenter video ad with an AI agent card
- Format: a person speaks to camera; a dark-blue, round-cornered card sits above the presenter (9:16) or behind them (16:9) and shows the AI agent talking (orb, voice waveform, words appearing as it speaks).
- Card source and exports live in `ad-card/`:
  - `ad-card/highvance-ai-card.html`: live reference page and spec for the editor (published at https://claude.ai/artifact/7d4zXGRV4ZGoJJGzSbsYvD).
  - `ad-card/exports/`: transparent PNG, ProRes 4444 alpha MOV (1120 × 720), VP9 alpha WebM, and a green-screen MP4 for CapCut.
- Card specs: 960 × 560, 36 px corners, navy #071A45, royal #0B2F86, signal blue #2F7BFF, ice #9CC8FF, white, live dot #FF5470. Fonts: Plus Jakarta Sans and IBM Plex Mono. 10-second loop: speaking, listening, clear.
- The agent's line on the card is a **placeholder** ("Hi Priya, this is HighVance AI. Your demo is booked for Thursday, 4 PM. Shall I send the details on WhatsApp?"). Replace it with the real script.
- The wordmark on the card is typed text; swap in the real logo when available.
- The card work is in PR https://github.com/officialsumitchaudhary-lab/Ai-voice-agent/pull/3.

## Campaign in progress: study-abroad motion graphic ad (54 s)
- Source and exports in `ad-video/study-abroad/` (`build.sh` rebuilds everything; `README.md` explains the files).
- Script beats: hook (1 lakh leads a week) → pain (every lead goes to 5 consultancies) → the real call (from 0:14) → "8 SECONDS" stat with a silent beat → reframe + "Book a Demo".
- The call is the founder's real recording (Aarushi calling Sumit about a Master's in Germany, 2:40, Hinglish). The ad uses a 32 s in-order cut (greeting → eligibility → IELTS → free counselling offer); a full-call version also exists. Transcript, cut list and tags live in `ad-video/study-abroad/call/transcript.json`.
- The founder's script listed the URL as "hiighvance.com"; the ad uses highvance.in. Confirm.
- The older `ad-card/` card uses Plus Jakarta Sans, #071A45 and #2F7BFF. Update it to the brand fonts and colours above before reusing it.

## Campaign in progress: omnichannel Reel "Your business has amnesia" (produced, 45 s)
- Script/prompt in `ad-video/omnichannel/prompt.md`: one customer (Ananya) repeats herself on 4 channels and buys elsewhere; replayed with Highvance's shared memory. Built for Instagram reach: comment trigger ("A or B?"), tag prompt, "Comment AUDIT" lead magnet (free mystery-shop audit), seamless loop.
- Founder confirmed (Oct 2026): all features are live (instant callback, booking, WhatsApp/email follow-up, analytics, lead scoring, CRM sync) and memory is centralised across every channel. The founder handles AUDIT requests manually.
- Built in `ad-video/omnichannel/` (9:16 + 1:1, -14 LUFS, seamless loop). Still pending: the real product recording of the AI memory line for 0:19.5–0:25 (slot left clear; `VOICE=... ./build.sh`).

## Marketing principles for HighVance
- Show the product working. A real recording of the agent handling a call beats any claim.
- Hook in the first 2–3 seconds, built around a problem the buyer already feels (for example missed calls or slow follow-up).
- One message and one CTA per ad. Make 3–5 hook variants of each video rather than one polished ad.
- Never state numbers (pick-up rates, savings, response times, client counts) unless the founder has confirmed them.
- Every paid campaign needs tracking set up before spend: Meta Pixel plus Conversions API, and a clear lead event.
- Speak to Indian business owners plainly. Price in ₹, and show WhatsApp and local-language support only if the product really does it.
