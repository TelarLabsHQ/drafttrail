# DraftTrail

Free writing-process recorder by Telar Labs. Students write in DraftTrail, download a `.drafttrail` file and hand it in;
teachers open the files to see flags, a timeline and a replay. Nothing is uploaded.

- `public/write/` – student writing page (records edits, autosaves on the device, downloads the .drafttrail file)
- `public/review/` – teacher review page (opens .drafttrail files in the browser)
- `public/assets/drafttrail-core.js` – rebuilds text from the recording and analyzes it
- `tools/build.py` – builds the information pages

## Cloudflare Pages settings
- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `public`
