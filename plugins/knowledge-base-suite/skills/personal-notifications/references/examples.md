# Worked example: same payload, three verbosity levels

Input payload (movies domain, 3 items):

```json
{
  "domain": "movies",
  "intro": "3 new movies found this week that might interest you.",
  "items": [
    {
      "title": "Dune Part Three",
      "summary": "Sci-fi sequel, practical-effects heavy like the last two.",
      "facts": {"showtimes": ["7:30pm", "10:00pm"], "cinema": "Cine Colombia Santa Fe"},
      "icon": "🎬"
    },
    {
      "title": "The Long Winter",
      "summary": "Slow-burn drama, well reviewed but not really your usual genre.",
      "facts": {"showtimes": ["8:00pm"], "cinema": "Cinemark Titan Plaza"},
      "icon": "🎬"
    },
    {
      "title": "Circuit Breaker",
      "summary": "Techno-thriller with a heist plot, gets good early reviews.",
      "facts": {"showtimes": ["6:15pm", "9:00pm"], "cinema": "Cine Colombia Santa Fe"},
      "icon": "🎬"
    }
  ]
}
```

Config: `language: es`, `style_notes: "Keep it light and quick, like a friend texting a recommendation. No formal sign-offs."`

## `verbosity: terse`, `emoji: some`

```
3 películas nuevas: 🎬 Dune Part Three (Cine Colombia Santa Fe, 7:30/10pm) · 🎬 The Long Winter (Cinemark Titan Plaza, 8pm) · 🎬 Circuit Breaker (Cine Colombia Santa Fe, 6:15/9pm).
```

One line, most essential fact folded in, no separate facts list — a glance, not a read.

## `verbosity: casual`, `emoji: some`

```
3 películas nuevas esta semana que te podrían interesar:

🎬 *Dune Part Three* — secuela de ciencia ficción, con muchos efectos prácticos como las anteriores. 7:30pm, 10:00pm en Cine Colombia Santa Fe.

🎬 *The Long Winter* — drama lento, bien calificada pero no muy tu estilo habitual. 8:00pm en Cinemark Titan Plaza.

🎬 *Circuit Breaker* — thriller tecnológico con atraco, buenas críticas tempranas. 6:15pm, 9:00pm en Cine Colombia Santa Fe.
```

Note the icon sits on each item (per "some"), not on the intro line — the intro only gets decorated at `emoji: heavy`. `*asterisks*` follow Telegram's own Markdown for bold.

## `verbosity: detailed`, `emoji: none`

```
Esta semana encontramos 3 películas nuevas en cines que podrían interesarte, según tus gustos anteriores.

Dune Part Three
Secuela de ciencia ficción, con un fuerte uso de efectos prácticos, igual que las dos anteriores.
- Horarios: 7:30pm, 10:00pm
- Cine: Cine Colombia Santa Fe

The Long Winter
Drama de ritmo lento, bien calificada por la crítica, aunque no es exactamente el género que sueles ver.
- Horarios: 8:00pm
- Cine: Cinemark Titan Plaza

Circuit Breaker
Thriller tecnológico con trama de atraco, buenas críticas iniciales.
- Horarios: 6:15pm, 9:00pm
- Cine: Cine Colombia Santa Fe
```

With `emoji: none`, no icon is used even though the payload supplied one — facts get plain dash bullets, no emoji markers anywhere.

## Config bootstrap example

If a brand-new domain `apartments` sends its first notification with no entry in `_notification-config.json`, this skill writes:

```json
{
  "apartments": {
    "channel": "telegram",
    "language": "en",
    "verbosity": "casual",
    "emoji": "some",
    "style_notes": ""
  }
}
```

— a direct copy of `_default` — before formatting the message, so there's now a concrete, editable entry for that domain instead of a silent fallback.
