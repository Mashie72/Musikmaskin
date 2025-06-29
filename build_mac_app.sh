#!/bin/bash

# === KONFIGURATION ===
APP_NAME="Musikmaskin"
SCRIPT="Musikmaskin.py"
ICON_PNG="ikon.png"
ICONSET_DIR="${APP_NAME}.iconset"
ICNS_FILE="${APP_NAME}.icns"
DMG_DIR="${APP_NAME}-dmg"

# === 1. Skapa .icns från .png ===
mkdir -p "$ICONSET_DIR"
sips -z 16 16     "$ICON_PNG" --out "$ICONSET_DIR/icon_16x16.png"
sips -z 32 32     "$ICON_PNG" --out "$ICONSET_DIR/icon_16x16@2x.png"
sips -z 32 32     "$ICON_PNG" --out "$ICONSET_DIR/icon_32x32.png"
sips -z 64 64     "$ICON_PNG" --out "$ICONSET_DIR/icon_32x32@2x.png"
sips -z 128 128   "$ICON_PNG" --out "$ICONSET_DIR/icon_128x128.png"
sips -z 256 256   "$ICON_PNG" --out "$ICONSET_DIR/icon_128x128@2x.png"
sips -z 256 256   "$ICON_PNG" --out "$ICONSET_DIR/icon_256x256.png"
sips -z 512 512   "$ICON_PNG" --out "$ICONSET_DIR/icon_256x256@2x.png"
sips -z 512 512   "$ICON_PNG" --out "$ICONSET_DIR/icon_512x512.png"
cp "$ICON_PNG" "$ICONSET_DIR/icon_512x512@2x.png"

iconutil -c icns "$ICONSET_DIR" -o "$ICNS_FILE"

# === 2. Bygg med PyInstaller ===
pyinstaller "$SCRIPT" \
  --windowed \
  --name "$APP_NAME" \
  --icon="$ICNS_FILE"

# === 3. Skapa .dmg med create-dmg (kräver npm install -g create-dmg) ===
mkdir -p "$DMG_DIR"
create-dmg \
  "dist/$APP_NAME.app" \
  --overwrite \
  --dmg-title="$APP_NAME" \
  --app-drop-link \
  "$DMG_DIR"

# === Klart ===
echo "✅ $APP_NAME byggd som .app och .dmg!"
echo "📁 Se: $DMG_DIR/$APP_NAME.dmg"
