# 🍈 Musk Melon

An open-source, AI-powered collaborative workspace — docs, wikis, databases and
kanban boards in one app — for macOS, Windows, Linux, iOS and Android.

> **Musk Melon is a fork of [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy)**
> (commit `5cf3a36`), rebranded under the terms of the
> [GNU AGPL-3.0](LICENSE). All credit for the original work goes to AppFlowy
> and its contributors. "AppFlowy" is a trademark of AppFlowy, Inc.; Musk Melon
> is not affiliated with or endorsed by AppFlowy. The upstream README is kept at
> [doc/UPSTREAM_APPFLOWY_README.md](doc/UPSTREAM_APPFLOWY_README.md).

## What changed from AppFlowy

| | AppFlowy | Musk Melon |
|---|---|---|
| Display name (UI, window title, launchers) | AppFlowy | Musk Melon |
| Product / binary name | `AppFlowy`, `AppFlowy.app`, `AppFlowy.exe` | `MuskMelon`, `MuskMelon.app`, `MuskMelon.exe` |
| Bundle / application ID | `io.appflowy.appflowy`, `com.appflowy.appflowy.flutter` | `com.muskmelon.muskmelon` |
| Linux D-Bus / Flatpak ID | `io.appflowy.AppFlowy` | `com.muskmelon.MuskMelon` |

All of it is applied by [`rebrand_musk_melon.py`](rebrand_musk_melon.py), which
is idempotent — re-run it after pulling upstream AppFlowy changes:

```bash
python3 rebrand_musk_melon.py
```

### Intentionally unchanged

- **Code identifiers** — Dart package `appflowy`, classes like `AppFlowyTheme`,
  Rust crates. Renaming them is cosmetic and would make upstream merges painful.
- **External dependencies** — `appflowy_editor`, `appflowy_board`, AppFlowy-Collab
  and AppFlowy-Cloud crates are fetched from AppFlowy's repositories.
- **Sync backend** — "AppFlowy Cloud" and its `*.appflowy.cloud` servers, the
  `appflowy-flutter://` sign-in callback, and the sign-in terms/privacy text.
  Musk Melon still uses AppFlowy's backend until you self-host
  [AppFlowy-Cloud](https://github.com/AppFlowy-IO/AppFlowy-Cloud) and point the
  app at it (Settings → Cloud → Self-hosted).
- **Android `namespace`** — must match the Kotlin package of `MainActivity`;
  the `applicationId` is what identifies the app on devices and stores.

### Still to do before shipping

- [ ] Replace logos and icons (`frontend/resources/flowy_icons`,
      `frontend/appflowy_flutter/assets/images`, platform `AppIcon`/`mipmap`/`.ico`
      sets, `doc/imgs`). They are AppFlowy's trademarked artwork.
- [ ] Replace in-app links to AppFlowy's website, docs and community.
- [ ] Decide on a sync backend (self-hosted AppFlowy-Cloud or local-only).

## Building

Musk Melon builds exactly like AppFlowy (Flutter + Rust via `cargo-make`):

```bash
cd frontend
cargo make appflowy-flutter-deps-tools
cargo make --profile development-mac-arm64 appflowy-dev   # pick your platform profile
```

See AppFlowy's
[build-from-source guide](https://docs.appflowy.io/docs/documentation/appflowy/from-source)
for per-platform prerequisites.

## License

[GNU Affero General Public License v3.0](LICENSE). If you distribute Musk Melon
or run a modified version as a network service, you must make its complete
source available under the same license.
