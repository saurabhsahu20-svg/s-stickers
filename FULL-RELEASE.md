# Full S Stickers v2.4.0 release

The repository main branch contains the earlier generated collection, not the complete 2,251 sticker project. The full source ZIP is required for this release.

1. Open Releases > Draft a new release. Create tag v2.4.0 targeting main.
2. Attach the exact file S-Stickers-v2.4.0-Regional-Idioms-WhatsApp-Source.zip (SHA-256 3cafe1132aa4f1c1f5dc30a4784a038d1fa26e4d0fae6cbab208519bafa2c927).
3. Mark pre-release until tested on device, then Publish release. The dedicated workflow builds the complete source and uploads the APK and checksum to the same release. It also supports manual dispatch after the source has been uploaded.
4. For a signed in-place update, configure repository Actions secrets S_STICKERS_KEYSTORE_BASE64, S_STICKERS_KEYSTORE_PASSWORD, S_STICKERS_KEY_ALIAS and S_STICKERS_KEY_PASSWORD using the private key matching the installed version. Never publish the key. Without these secrets a test APK is produced and a fresh installation may be necessary.

The workflow verifies all 2,251 PNGs and WebPs, 103 pack definitions, the APK signature and checksums. Device and WhatsApp import testing remain necessary.
