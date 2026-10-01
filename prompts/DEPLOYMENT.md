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
2. If the platform plays a welcome message, remove the opening block from the prompt so it isn't said twice.
