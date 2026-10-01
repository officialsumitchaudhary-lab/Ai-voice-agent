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
