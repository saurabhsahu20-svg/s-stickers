# S Stickers

Native Android offline sticker gallery, version 1.0.0. Includes 16 categories and 1,000 generated 512×512 transparent PNG sticker variations. Artwork is original procedural drawing, not a collection of individually AI-painted designs. The build generates and validates the image files before packaging.

Features: category browsing, text search, favorites, recently used, PNG preview, Android share sheet and Save PNG. Sharing sends an image to compatible apps; native WhatsApp sticker-pack installation, GIF animation, custom pack creation and keyboard integration are not implemented yet.

## Build
Use JDK 17, Android SDK 35, Gradle 8.9, Python 3 and Pillow (pip install Pillow==11.3.0). Run `gradle :app:assembleDebug`. The Android APK workflow also builds on pushes and manual dispatch. Download the debug APK artifact from Actions after a successful run. Debug signing is for testing; production releases need a consistent private signing key (never commit it).

No network or storage permissions are required. User favorites and recent history stay on the device. No ads or trackers.

## Notes
The generator uses a small set of illustration templates and many palette, layout and accent variations. Validation checks the PNG count, dimensions, alpha channel and unique hashes; visual quality and compatibility still require device testing.

## v1.1.0 — Desi Boli
Adds 235 original conversational PNGs across 21 language and cultural greeting packs (total 1235). Native scripts plus Roman captions where available; Sindhi currently Roman only. Dedicated Desi tab and existing search support. Colloquial phrasing varies by region; native speaker review is recommended. Jain Greetings is a cultural pack, not a language. Build requires Ubuntu fonts-noto-core and Pillow with RAQM. Existing 1,000 sticker IDs are preserved.

## v1.2.0 — Chhattisgarhi Daily Life
53 additional 512px transparent conversation PNG designs in six Chhattisgarhi topic packs. Preserves previous 1,235 sticker IDs. Adds themed hand-drawn pictograms and native/Roman captions. Three direct threat phrases and one alcohol-themed phrase in the supplied reference were replaced with nonviolent everyday alternatives. Only visible phrases were used. Total build-time catalog: 1288.

## v1.3.0 — Punjabi and Bengali Daily Life
Adds 73 512px RGBA stickers in 10 topic packs (1361 total), preserving all previous IDs. The native text is dominant, with high-contrast Hindi meanings and Roman pronunciations. Three threats and an alcohol-oriented phrase were replaced with nonviolent everyday phrases; one harsh whereabouts phrase was softened. Punjabi native script and Hindi gloss were added to the reference phrases. Local speaker review is recommended. CI checks packaged asset count and APK signature.

## v1.4.0 — Big & Bold
Adds 59 screenshot-derived Mumbai Tapori, Gujarati and Telugu conversation designs, with native, Roman and Hindi text. Overlapping Telugu screenshots are counted once. 1420 total assets, existing IDs unchanged. Enlarges legacy captions, Desi native/Roman text and multilingual text limits, with automatic fitting for long text. Two-column larger grid, 256px thumbnails and scrollable large preview. Dialect translations are not independently certified.
