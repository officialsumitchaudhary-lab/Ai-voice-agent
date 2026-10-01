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
