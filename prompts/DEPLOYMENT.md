# Deployment checklist (outside the prompt)

1. **`{available_slots}`.** Send ready-to-speak lines, one per slot, e.g.
   `Monday, twelve October, shaam paanch baje`. Test calls got three days on one date and no times.
2. **`{counsellor_gender}`.** Add it (`female` / `male`) so verbs agree with the counsellor's name.
3. **KB entries needed** so she has real answers under pressure:
   Highvance's own scholarships (yes/no, what), kinds of scholarships, how shortlisting works,
   Germany intake names and months, job-prospect wording (process only), post-call fields.
4. **Model.** Many failures broke explicit rules. Use a strong model, temperature 0.5 or lower.
5. **Transcriber.** Hindi arrives in Devanagari; the prompt handles it, but a Romanized or
   Hinglish STT setting reduces script leaks further.

## Meera

1. **Knowledge base:** `prompts/meera-kb.md` (demo data). Discounted amounts are precomputed for
   a twenty percent discount, so keep `{discount_percent}` at twenty or update the KB table.
2. **Demo call values:** `{learner_name}` Rohan, `{track_name}` Data Analytics, `{trial_day}` five,
   `{trial_end_date}` Sunday, eleven October, `{lessons_completed}` two, `{last_active}` three days ago,
   `{discount_percent}` twenty.
3. **`{trial_end_date}`** already in spoken words; **`{discount_percent}`** may be digits.
4. If the platform plays a welcome message, she continues from it; otherwise she opens herself.
5. **Re-upload `meera-kb.md` to the platform.** Test calls quoted thirty thousand and twelve thousand
   rupees and "twelve September". None of these are in the KB, so the platform has an old KB or none.
6. **`{trial_end_date}` must be a future date**, in words, e.g. Sunday, eleven October.
7. **`{track_name}`**: the feed sent "Data analystics". Send "Data Analytics".
8. **End-of-turn wait.** She answered "hmm actually…" within a second. Raise the endpointing /
   silence threshold to about one second so callers can finish.

## Tanvi

1. **Voice engine.** Use the same voice engine as Aarushi. The prompt is Romanized Hinglish; Cartesia
   Sonic 3.5 was the reason for the old Devanagari rule.
2. **Knowledge base:** `prompts/tanvi-kb.md` (v1.1 demo). Upload only this file.
3. **New variable:** `{fasting_start_time}`, the last time to eat in Romanized Hindi (e.g. raat das baje), worked out by the platform from the slot.

## Neha

1. **Voice engine.** Same as Aarushi: the prompt is Romanized Hinglish, not Devanagari.
2. **`{available_slots}`.** Send three or more ready-to-speak site visit slots, e.g. `Shanivaar subah das baje`.
   The old prompt hard-coded Saturday, Sunday and Monday slots.
3. **Knowledge base:** `prompts/neha-kb.md` (v1.1 demo). Upload only this file.
4. **Callback number:** the KB has none until a real one exists. Add it to Section 1 before go-live.
5. **Welcome message:** capitalise the caller's name (the test call said "sumit").
6. **End-of-turn wait:** raise the silence threshold to about one second; Neha cut in on "ah mujhe…".
7. **Knowledge base retrieval:** set retrieval to return all of Section 4 (or paste Section 4 into the prompt), so she sees every project before deciding fit.
8. **Model:** Devanagari leaks, a repeated question, an invented BHK and digits all broke explicit rules. Use a stronger model, temperature 0.5 or lower, and a Hinglish STT setting if available.


## Monica (ZICA ZIMA Hegde Nagar)

1. **Language confirmation:** turn OFF any platform setting that asks "which language are you comfortable in" on a detected
   language change. The prompt asks once and locks the language; the platform question caused repeated asks in testing.
   If the platform auto-switches, set its threshold as high as allowed (switch after two or more turns, not one word).
2. **Welcome message:** no commas inside the name or phrases ("calling, from", "quickly, connect" cause pauses).
   Send `{lead_name}` in proper case and `{course_interest}` as it is spoken (VFX, not vfx).
3. **`{available_slots}`:** send spoken text, e.g. `Saturday, eleven in the morning`. Test calls received digits and am/pm.
4. **Knowledge base:** upload `zica-kb.md`; the prompt matches interests to its programme names.
5. **Endpointing:** about one second, so callers can finish before Monica speaks.
6. **Hindi language mode (root cause of Devanagari replies):** Devanagari kept appearing even with strong prompt rules, so the
   platform is most likely switching to a Hindi (hi-IN) mode that injects "respond in Hindi" or a Devanagari voice.
   Do NOT list Hindi as an auto-switch language. Keep English as the only platform language, and let the prompt handle Hindi as Romanized
   Hinglish on the same voice.
7. **Speech-to-text languages:** lock recognition to English and Hindi. Test calls returned Gurmukhi and Odia text
   for Hindi speech ("ਸੋ ਹਿੰਦੀ", "ਮਤਲਬ"), which the agent then misreads.
8. **No Sunday slots:** the centre is open Monday to Saturday, eight in the morning to eight at night. `{available_slots}` must stay inside those hours.
9. **Cold calls:** the number source is fixed in the prompt ("from colleges"), so `{lead_source}` is no longer sent. Scrub every
   list against DND before a campaign and honour removal requests in the dialer the same day.
10. **Referrals:** add post-call extraction fields for the referred student's name, number and best time to call, and route them
   to the counsellor's callback list. Monica tells the caller the counsellor will call, so someone must.

## Neha (SRVA, NMIMS Online MBA)

1. **Files:** system prompt `srva-neha.md`, knowledge base `srva-neha-kb.md`.
2. **Welcome message:** `Hello, am I speaking with {lead_name}?` The prompt continues from it. Proper-case names, no stray spaces before punctuation.
3. **Calendar:** connect the counsellor calendar so the agent can check a time and book it. Without it she notes the preferred time and says the counsellor confirms.
4. **Hangup message:** keep it empty or one short line. The prompt already closes with a goodbye.
5. **Languages:** English and Hindi only. Hindi must stay Romanized Hinglish; if Devanagari appears, check the platform's Hindi mode or voice.
6. **Post-call fields:** outcome, qualification, percentage, specialisation, counsellor slot, callback time, email.
