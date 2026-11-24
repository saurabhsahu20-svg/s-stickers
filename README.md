# S Stickers

Native Android offline sticker gallery, version 1.0.0. Includes 16 categories and 1,000 generated 512×512 transparent PNG sticker variations. Artwork is original procedural drawing, not a collection of individually AI-painted designs. The build generates and validates the image files before packaging.

Features: category browsing, text search, favorites, recently used, PNG preview, Android share sheet and Save PNG. Sharing sends an image to compatible apps; native WhatsApp sticker-pack installation, GIF animation, custom pack creation and keyboard integration are not implemented yet.

## Build
Use JDK 17, Android SDK 35, Gradle 8.9, Python 3 and Pillow (pip install Pillow==11.3.0). Run `gradle :app:assembleDebug`. The Android APK workflow also builds on pushes and manual dispatch. Download the debug APK artifact from Actions after a successful run. Debug signing is for testing; production releases need a consistent private signing key (never commit it).

No network or storage permissions are required. User favorites and recent history stay on the device. No ads or trackers.

## Notes
The generator uses a small set of illustration templates and many palette, layout and accent variations. Validation checks the PNG count, dimensions, alpha channel and unique hashes; visual quality and compatibility still require device testing.
