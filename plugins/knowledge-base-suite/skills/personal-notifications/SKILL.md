---
name: personal-notifications
description: Formats a domain skill's JSON output into a human-ready notification (tone, verbosity, emoji, language per domain, using ~/knowledge-base/_notification-config.json) and delivers it to Al on Telegram through his bot @AlClawMainBot with the Telegram MCP. ANY skill that needs to notify Al about domain data (new recipes, movies, job listings, apartment matches, etc.) or answer a request he sent through Telegram MUST use this skill. Use it whenever composing or sending a notification, digest or summary message for Al, or when a domain has no notification config yet and needs a default bootstrapped.
---

# Personal Notifications — Formatting Standard

This skill turns structured data into a message a human would actually want to read and sends it to Al on Telegram. It does **not** know anything about what a "movie" or a "job opportunity" is — it only knows how to take labeled data, present it with the right tone, length, and language for its domain, and deliver it.

Core principle, same as `personal-knowledge-base`: **stay domain-blind**. All domain judgment — what's worth mentioning, how items should be grouped, why they matter — belongs to the caller (the domain skill). This skill only makes presentational decisions: layout, tone, verbosity, emoji, language.

This skill sends the finished text (see Delivery) and returns the delivery result to the caller. The caller remains responsible for updating `report_status` in the knowledge base once delivery is confirmed.

## Input contract

The caller provides a domain name and a JSON payload:

```json
{
  "domain": "movies",
  "intro": "3 new movies found this week that might interest you.",
  "items": [
    {
      "title": "Dune Part Three",
      "summary": "Sci-fi sequel, practical-effects heavy like the last two.",
      "facts": {
        "showtimes": ["7:30pm", "10:00pm"],
        "cinema": "Cine Colombia Santa Fe"
      },
      "icon": "🎬"
    }
  ]
}
```

- `domain` — required. Used to look up formatting config (see below).
- `reply_to` — optional. Telegram message id of Al's message this notification answers (for requests he sent to the bot); the message is sent as a reply to it.
- `intro` — optional. The caller's own words for an overview/framing line. Used close to as-is — this skill fits it into the target language and layout, but doesn't reinterpret or add domain judgment to it. Omit it entirely if there's nothing worth framing (e.g. a single obvious item).
- `items` — required, always a list, even for a single item. No special-casing single vs. multi-item messages — same contract either way.
- Each item:
  - `title` — required.
  - `summary` — required, one or two sentences, caller's own words.
  - `facts` — optional, a flat key/value object. Rendered generically: keys are humanized (`release_date` → "Release Date"), values are displayed as-is (a list becomes a comma list or sub-bullets depending on verbosity — see below). This skill does not need to understand what a fact *means* to display it.
  - `icon` — optional, a single emoji the caller chooses to represent this item (e.g. 🎬 for a movie, 💼 for a job listing). This is how domain-relevant emoji get used **without** this skill needing domain knowledge — the caller supplies the icon if it wants one used; this skill only decides *whether* to use it, based on the domain's emoji setting.

## Output

A single finished message string (or, if it would exceed Telegram's message-length limit — currently 4096 characters — multiple sequential message strings, split cleanly between items, never mid-item), sent as described in Delivery. The caller gets back the sent message ids, or the reason delivery failed.

## Per-domain config (`~/knowledge-base/_notification-config.json`)

Lives alongside the knowledge base's other top-level files, but is **owned and written exclusively by this skill** — `personal-knowledge-base` never reads or writes it, and this skill never reads or writes `_domains.json` or anything inside a domain folder. Same independence principle as domains not coupling to each other, one level up.

```json
{
  "movies": {
    "channel": "telegram",
    "language": "es",
    "verbosity": "casual",
    "emoji": "some",
    "style_notes": "Keep it light and quick, like a friend texting a recommendation. No formal sign-offs."
  },
  "job-opportunities": {
    "channel": "telegram",
    "language": "en",
    "verbosity": "professional",
    "emoji": "none",
    "style_notes": "Straightforward and factual. Lead with the role and company, not commentary."
  },
  "_default": {
    "channel": "telegram",
    "language": "en",
    "verbosity": "casual",
    "emoji": "some",
    "style_notes": ""
  }
}
```

Fields:
- `channel` — which delivery channel this formatting targets. Currently only `telegram` is used in practice, but the field exists so other channels can be added later without changing the schema. Formatting rules below assume Telegram's rendering (its own lightweight Markdown: `*bold*`, `_italic_`) unless a domain specifies otherwise.
- `language` — the language this skill's own generated text (labels, connective phrasing, structural lines) is written in. **This skill does not machine-translate the caller's content** — `intro`, `summary`, and `facts` values are assumed to already be written by the caller in this domain's configured language. If a domain's `intro`/`summary` text doesn't match its configured `language`, that's a caller-side inconsistency to fix, not something this skill corrects.
- `verbosity` — one of `terse`, `casual`, `detailed` (see Formatting rules).
- `emoji` — one of `none`, `some`, `heavy` (see Formatting rules).
- `style_notes` — optional freeform prose. When present and specific, it **refines and can override** what `verbosity`/`emoji` would otherwise produce — e.g. `verbosity: casual` normally includes a facts list, but a style note saying "keep this to one short sentence, no bullet points" wins. An empty `style_notes` means the structured fields alone determine the output. Same precedence logic as `personal-knowledge-base`'s "item file overrides index cache" — the more specific, purpose-written instruction outranks the generic default.

### Bootstrapping missing config

If the caller's `domain` has no entry in `_notification-config.json`:
1. If the file doesn't exist yet, create it with just `_default` (the baseline shown above).
2. Copy `_default`'s values into a new entry under the domain's name, setting `language` to the language the caller's content is written in (e.g. `es` for recipes), and save the file.
3. Format the message using those (freshly copied) values.

This makes the domain's config visible and editable going forward, rather than silently falling back to `_default` forever with nothing for the user to tweak.

## Formatting rules

### Verbosity

- **`terse`** — one line per item. Title + the single most essential fact folded into the line, no separate facts list, intro dropped or reduced to a few words. Built for a quick glance, not reading.
- **`casual`** — a short intro line (if provided), then per item: bolded title, one-line summary, facts rendered as a brief inline list. Friendly, conversational connective phrasing.
- **`detailed`** — a full intro paragraph (if provided), then per item: bolded title, full summary, every fact on its own line with a humanized label. Built for content the user actually wants to sit with.

### Emoji

- **`none`** — no emoji anywhere, including no fallback markers. Use plain punctuation/dashes for structure instead.
- **`some`** — one emoji per item at most. Use the item's `icon` if the caller provided one; if not, fall back to a single generic structural marker (e.g. `•`) rather than inventing a domain-themed emoji this skill has no basis to choose.
- **`heavy`** — more expressive: the item's `icon` (or generic marker) plus light additional structural emoji for sections (e.g. a header emoji on the intro line). Still never invents domain-meaning emoji beyond what `icon` supplies — "heavy" means more frequent use of what's available, not guessing at new ones.

### `facts` rendering

- Humanize keys: `snake_case` or `camelCase` → `Title Case With Spaces`.
- Scalar values render as-is.
- List values: comma-joined inline for `terse`/`casual`, one sub-bullet per value for `detailed`.

### Multi-item messages

Same contract as single-item — just more entries in `items`. Assemble as one message: intro line (per verbosity), then each item in order, per verbosity/emoji rules above. If assembling would exceed Telegram's ~4096-character limit, split into multiple messages at item boundaries — never truncate mid-item, and repeat a short "(continued)" marker at the start of subsequent chunks rather than repeating the full intro.

### Language

Write all of this skill's own structural text (intro framing words if the caller didn't supply exact phrasing, "(continued)" markers, humanized fact labels if they need connective words) in the domain's configured `language`. Caller-supplied content (`title`, `summary`, `intro` text, `facts` values) is passed through as given — see the `language` field note above.

## Delivery (Telegram)

Al receives notifications from his bot through the Telegram MCP:

| Setting | Value |
| --- | --- |
| MCP account | `bot` (the bot **@AlClawMainBot**, id 8731706984) |
| Recipient | Al — Telegram user id `7812154300` (phone +34 605 073 551) |

- Send each message chunk with `send_message(account="bot", chat_id=7812154300, message=<text>, parse_mode="md")`, in order; add `reply_to` on the first chunk when the caller passed one.
- Always use the user id as `chat_id`: a bot can't open a chat by phone number, only write to users who have started it (Al already has).
- Never send from the `default` account (Al's own user account) and never to any other chat.
- If `_notification-config.json` has a `_delivery` entry, its `account` and `chat_id` override the table above.
- Sending fails (MCP missing, bot blocked, network) → don't retry in a loop; return the formatted text and the error to the caller so it can show it in the session.

## Workflow summary

1. Read `_notification-config.json`. If the domain has no entry, bootstrap it from `_default` (see above) and save.
2. Apply `verbosity`, `emoji`, `language`, and `style_notes` (refining/overriding the structured fields where specific) to the payload.
3. Render `intro` (if present) and each item per the rules above.
4. Assemble into one message, splitting at item boundaries only if needed for length.
5. Send it as described in Delivery and return the message ids (or the error) to the caller. Do not touch the knowledge base.

See `references/examples.md` for the same payload rendered at all three verbosity levels.
