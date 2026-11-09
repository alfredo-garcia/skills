# Extractors by source

Every extractor aims for: title, ingredient lines (as written), steps, servings, times, author, URL, language, best image. Combine sources when useful (caption + transcript).

## Screenshot or photo from anywhere

Any app or site: Instagram, TikTok, WhatsApp, a web page, a PDF viewer, a TV screen, a book.

- Read it directly (vision). Several screenshots sent together = one input, in order.
- Identify the origin from what's visible (app UI, handle, URL bar, watermark) for `source.type`, `author` and `url`; unknown → `own`.
- Text cut at the edge or "ver más" collapsed → ask for the next screenshot in conversation; unattended, note it in `doubts`.
- Use the screenshot as the recipe photo only if it shows the dish; otherwise crop the dish if there is one, or leave `photo` empty.

## Instagram link (post, reel)

Shortcode from `/p/<code>/`, `/reel/<code>/`, `/reels/<code>/` or `/tv/<code>/`. Try in order and stop when you have the recipe:

1. **Public embed page**, usually readable without login:
   `curl -sL -A "Mozilla/5.0" "https://www.instagram.com/p/<code>/embed/captioned/"`
   Take the caption text (the element with class `Caption`; strip the handle prefix and hashtags) and the image (`img.EmbeddedMediaImage` src) as the photo. Author = handle shown in the embed.
2. **yt-dlp** (reels and video posts):
   `yt-dlp --skip-download --write-info-json --write-thumbnail -o "/tmp/ig/%(id)s" "<url>"` → `description` in the `.info.json`, thumbnail as the photo.
   If the caption lacks quantities or steps and the video narrates them: `yt-dlp -x --audio-format mp3 -o "/tmp/ig/%(id)s.%(ext)s" "<url>"`, then transcribe with faster-whisper (`pip install faster-whisper`; model `small`, `language="es"` or auto). Note "transcrito del audio" in `doubts`.
   Missing tools → `pip install yt-dlp`.
3. **Browser with Al's logged-in session** (Claude in Chrome, or Cowork's browser): open the post, expand the caption, read it, take a screenshot for the photo.
4. Nothing worked → ask Al for a screenshot (conversation) or leave the entry with reason "necesito captura o texto" (unattended).

These are unofficial routes and can stop working; if one fails, go to the next without retrying it.

## YouTube

- Video id from `watch?v=`, `youtu.be/` or `shorts/`.
- **Title and description**: `yt-dlp --skip-download --write-info-json "<url>"` or fetch the page; many channels put the full recipe in the description.
- **Transcript**: `yt-dlp --skip-download --write-auto-subs --sub-langs "es.*,en.*" --sub-format vtt -o "/tmp/yt/%(id)s" "<url>"` and read the `.vtt`. No subtitles → audio + faster-whisper as for Instagram.
- **Thumbnail**: `https://img.youtube.com/vi/<id>/maxresdefault.jpg` (fallback `hqdefault.jpg`).
- Author = channel. Times only if stated.

## Google Doc

- In the synced folder, rclone exports native Google Docs as `.docx`: `pandoc file.docx -t plain` or python-docx.
- A Docs link in conversation: Google Drive connector if available; otherwise ask Al to paste the text.
- `source.type: google-doc`.

## Web page

- Fetch it; prefer structured recipe data (JSON-LD `Recipe`), then visible text. `source.type: web`, author = site or byline.

## PDF

- `pdftotext` (or the pdf skill); scanned PDFs → read pages as images.

## Free text

- Parse directly. No URL → `source.type: own`, unless Al says it's family (`family`) or a book (`book`).
