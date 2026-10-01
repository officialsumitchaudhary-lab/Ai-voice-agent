# Deployment checklist (outside the prompt)

1. **First message.** Set the platform's first message to:
   `Hi, kya meri baat {lead_name} se ho rahi hai?`
   The current fixed opener says "abhi" and "ke regarding" and skips the identity check.
2. **`{available_slots}`.** Send ready-to-speak lines, one per slot, e.g.
   `Monday, twelve October, shaam paanch baje`. Test calls got three days on one date and no times.
3. **`{counsellor_gender}`.** Add it (`female` / `male`) so verbs agree with the counsellor's name.
4. **KB entries needed** so she has real answers under pressure:
   Highvance's own scholarships (yes/no, what), kinds of scholarships, how shortlisting works,
   Germany intake names and months, job-prospect wording (process only), post-call fields.
5. **Model.** Many failures broke explicit rules. Use a strong model, temperature 0.5 or lower.
6. **Transcriber.** Hindi arrives in Devanagari; the prompt handles it, but a Romanized or
   Hinglish STT setting reduces script leaks further.
