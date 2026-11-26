# StickU release and signing continuity

StickU is the new display name of S Stickers. Preserve application ID com.sstickers.app and use strictly increasing versionCode values. The current full collection is 1,843 stickers and 107 WhatsApp packs.

For the existing GitHub release tagged StickU, attach the complete asset named StickU-v2.6.1-Recovered-Source.zip. On Actions > StickU 2.6.1 Release Build, run the workflow on main with release_tag StickU. The workflow downloads that exact asset, checks counts, applies the app label, builds, verifies package and APK signature, and uploads the APK to the chosen release. A source-only release does not contain an APK.

Build tools are provisioned on GitHub Actions: JDK 17, Gradle 8.9, Android SDK platform 35, build tools 35.0.0, Python 3.12 and Pillow 11.3.0. No SDK archive needs to be kept on a chat computer.

For updates without uninstalling, retain the original signing keystore in an encrypted offline backup, and configure GitHub repository Settings > Secrets and variables > Actions with these repository secrets:
- S_STICKERS_KEYSTORE_BASE64
- S_STICKERS_KEYSTORE_PASSWORD
- S_STICKERS_KEY_ALIAS
- S_STICKERS_KEY_PASSWORD

Never commit the keystore or passwords to a public repository or release. A new key cannot sign an update to an existing installation signed with another key. If secrets are not configured, the workflow only produces a clearly named test APK. Device and WhatsApp import testing are required before treating a build as stable. Keep full source ZIPs in releases and back them up; the main branch legacy build is not the latest full collection.

The recovered compact ZIP preserves all WebP assets and restores omitted PNGs before validation. Use the new encrypted StickU PKCS12 key for future updates to the newly signed v2.6.0 test APK (versionCode 26); full v2.6.1 uses versionCode 27. Keep the private key and password in secure backups and repository secrets only. Never attach them to the release.
