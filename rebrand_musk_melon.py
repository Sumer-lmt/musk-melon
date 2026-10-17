#!/usr/bin/env python3
"""Rebrand the AppFlowy source tree as "Musk Melon".

Musk Melon is a fork of AppFlowy (https://github.com/AppFlowy-IO/AppFlowy),
licensed under AGPL-3.0. This script changes user-facing branding only:

  * display name  -> "Musk Melon"   (UI strings, window titles, launchers)
  * product/binary -> "MuskMelon"   (no space, so build/packaging scripts work)
  * bundle/app id -> com.muskmelon.muskmelon

Deliberately left untouched so the app still builds and syncs:
  * Dart/Rust identifiers and package names (package:appflowy/..., AppFlowyTheme)
  * external dependencies (appflowy_editor, AppFlowy-Collab, AppFlowy-Cloud crates)
  * "AppFlowy Cloud" (the real sync backend) and its *.appflowy.cloud URLs
  * the appflowy-flutter:// OAuth callback scheme registered with that backend
  * Windows URL-protocol registry keys

Idempotent: run it again after merging upstream changes.
Usage: python3 rebrand_musk_melon.py [repo_root]
"""
import re
import sys
from pathlib import Path

DISPLAY = "Musk Melon"
PRODUCT = "MuskMelon"
BUNDLE_ID = "com.muskmelon.muskmelon"
DBUS_ID = "com.muskmelon.MuskMelon"
COPYRIGHT = "Copyright © 2026 Musk Melon contributors. Based on AppFlowy (AGPL-3.0)."

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent).resolve()
FE = ROOT / "frontend"
APP = FE / "appflowy_flutter"

# Identifier-level rewrites applied to every targeted file, in order.
ID_RULES = [
    (re.compile(r"io\.appflowy\.AppFlowy"), DBUS_ID),
    (re.compile(r"/io/appflowy/AppFlowy/"), "/com/muskmelon/MuskMelon/"),
    (re.compile(r"com\.appflowy\.appflowy\.flutter"), BUNDLE_ID),
    (re.compile(r"(?:io|com)\.appflowy\.appflowy"), BUNDLE_ID),
    (re.compile(r"Copyright ©? ?\d{4} AppFlowy\.IO\. All rights reserved\."), COPYRIGHT),
    (re.compile(r"Copyright \(C\) \d{4} io\.appflowy\. All rights reserved\."), COPYRIGHT.replace("©", "(C)")),
    (re.compile(r'"CompanyName", "io\.appflowy"'), f'"CompanyName", "{DISPLAY}"'),
    (re.compile(r"^AppPublisher=AppFlowy-IO$", re.M), f"AppPublisher={DISPLAY}"),
    # Debian package names must be lowercase.
    (re.compile(r"^Package: AppFlowy$", re.M), "Package: musk-melon"),
    (re.compile(r"INFOPLIST_KEY_CFBundleDisplayName = AppFlowy;"),
     f'INFOPLIST_KEY_CFBundleDisplayName = "{DISPLAY}";'),
    # File/binary-name forms: AppFlowy.app, AppFlowy.exe, AppFlowyMutex, AppFlowy_0.2.9.deb ...
    (re.compile(r"(?<![A-Za-z0-9_.@-])AppFlowy(?=\.app\b|\.exe|\.desktop|Launcher|Mutex|_\d)"), PRODUCT),
]

# Filesystem paths to the binary: /usr/bin/AppFlowy, ./AppFlowy, $LIB/AppFlowy.
# Only applied on lines without a URL.
PATH_WORD = re.compile(r"(?<=/)AppFlowy(?![A-Za-z0-9_-]| Cloud)")

# The bare word "AppFlowy", excluding URLs/paths, longer identifiers, the
# AppFlowy Cloud backend and upstream repo names (AppFlowy-IO, AppFlowy-Collab).
WORD = re.compile(r"(?<![A-Za-z0-9_/.@-])AppFlowy(?![A-Za-z0-9_-]| Cloud|\.(?:io|IO|com)\b)")

# Lines where the word names a binary/package rather than a display label.
BINARY_LINE = re.compile(
    r"Exec|exec:|/usr/|/opt/|\$LIB|\.sh\b|Source:|Filename:|DefaultDirName|"
    r"BINARY_NAME|PRODUCT_NAME|Package:|CMD|test -e|file \./|\bcp |\bln |\brm |"
    r"Release/|DestName|BuildableName|path = "
)
PROTECTED_LINE = re.compile(r"HKCR|github\.com|flathub")


def brand_line(line: str, mode: str) -> str:
    # Android namespace must match the Kotlin package of MainActivity.
    if line.lstrip().startswith("namespace "):
        return line
    for pat, rep in ID_RULES:
        line = pat.sub(rep, line)
    if PROTECTED_LINE.search(line):
        return line
    if mode == "display":
        name = DISPLAY
    elif mode == "translation":
        # Only touch the value of `"key": "value"`, never the key.
        m = re.match(r'(\s*"[^"]*"\s*:\s*)(.*)', line, re.S)
        if not m:
            return line
        return m.group(1) + WORD.sub(DISPLAY, m.group(2))
    else:  # auto: binary name on build lines, display name elsewhere
        name = PRODUCT if BINARY_LINE.search(line) else DISPLAY
        if "://" not in line:
            line = PATH_WORD.sub(PRODUCT, line)
    return WORD.sub(name, line)


def process(path: Path, mode: str = "auto") -> bool:
    text = path.read_text(encoding="utf-8")
    new = "".join(brand_line(l, mode) for l in text.splitlines(keepends=True))
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def targets():
    for p in sorted((FE / "resources" / "translations").glob("*.json")):
        yield p, "translation"
    for p in sorted((APP / "assets" / "translations").glob("*.json")):
        yield p, "translation"
    for rel in [
        "lib/workspace/application/notification/notification_service.dart",
        "lib/shared/error_page/error_page.dart",
        "lib/mobile/presentation/home/mobile_home_page_header.dart",
        "lib/startup/tasks/windows.dart",
        "assets/template/readme.json",
        "assets/template/readme.afdoc",
        "ios/Runner/Info.plist",
        "android/app/src/main/AndroidManifest.xml",
        "windows/runner/main.cpp",
        "windows/runner/Runner.rc",
        "linux/my_application.cc",
    ]:
        yield APP / rel, "display"
    auto = [
        APP / "pubspec.yaml",
        APP / "android/app/build.gradle",
        APP / "windows/CMakeLists.txt",
        APP / "linux/CMakeLists.txt",
        APP / "macos/Runner/Configs/AppInfo.xcconfig",
        APP / "macos/Runner.xcodeproj/project.pbxproj",
        APP / "macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme",
        APP / "ios/Runner.xcodeproj/project.pbxproj",
        FE / "Makefile.toml",
        FE / "scripts/windows_installer/inno_setup_config.iss",
        FE / "scripts/docker-buildfiles/Dockerfile",
    ]
    auto += sorted((APP / "linux/packaging").rglob("make_config.yaml"))
    for d in ["linux_distribution", "linux_installer", "flatpack-buildfiles"]:
        auto += sorted(p for p in (FE / "scripts" / d).rglob("*") if p.is_file())
    for p in auto:
        yield p, "auto"


def rename_files():
    """Rename packaging files whose names carry the old ids."""
    for p in sorted(FE.joinpath("scripts").rglob("*"), key=lambda p: -len(p.parts)):
        name = p.name
        new = name.replace("io.appflowy.AppFlowy", DBUS_ID)
        if name == "AppFlowy.desktop":
            new = f"{PRODUCT}.desktop"
        if new != name:
            p.rename(p.with_name(new))
            print(f"renamed  {p.relative_to(ROOT)} -> {new}")


def main():
    changed = 0
    for path, mode in targets():
        if not path.is_file():
            print(f"missing  {path.relative_to(ROOT)}")
            continue
        try:
            if process(path, mode):
                changed += 1
                print(f"branded  {path.relative_to(ROOT)}")
        except UnicodeDecodeError:
            pass  # binary asset
    rename_files()
    print(f"\n{changed} files rebranded as {DISPLAY}.")


if __name__ == "__main__":
    main()
