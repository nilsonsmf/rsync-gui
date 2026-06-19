#!/usr/bin/env bash
set -euo pipefail

APP="rsync-gui"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="/opt/${APP}"
BIN_LINK="/usr/local/bin/${APP}"
DESKTOP_DIR="/usr/local/share/applications"
DESKTOP_FILE="${DESKTOP_DIR}/${APP}.desktop"
ICON_DIR="/usr/local/share/icons/hicolor/scalable/apps"
ICON_FILE="${ICON_DIR}/${APP}.svg"

info()  { echo -e "\033[1;34m*\033[0m $*"; }
ok()    { echo -e "\033[1;32m\xe2\x9c\x93\033[0m $*"; }
err()   { echo -e "\033[1;31m\xe2\x9c\x97\033[0m $*" >&2; }

if [ "$EUID" -ne 0 ]; then
    err "Please run as root: sudo ./install.sh"
    exit 1
fi

# ------------------------------------------------------------------ deps
info "Installing system dependencies..."
if command -v apt &>/dev/null; then
    apt-get update -qq && apt-get install -y -qq rsync python3 python3-venv python3-pip
elif command -v dnf &>/dev/null; then
    dnf install -y rsync python3 python3-virtualenv python3-pip
elif command -v pacman &>/dev/null; then
    pacman -Sy --noconfirm rsync python python-pip
elif command -v zypper &>/dev/null; then
    zypper --non-interactive install rsync python3 python3-venv python3-pip
else
    info "Unknown package manager. Ensure rsync, python3, python3-venv are installed."
fi
ok "System dependencies ready"

# ------------------------------------------------------------------ copy
info "Copying application to ${INSTALL_DIR}..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "${SRC_DIR}/src" "${SRC_DIR}/requirements.txt" "$INSTALL_DIR/"
ok "Application copied"

# ------------------------------------------------------------------ venv
info "Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/.venv"
"$INSTALL_DIR/.venv/bin/pip" install -q -r "$INSTALL_DIR/requirements.txt"
ok "Virtual environment ready"

# ------------------------------------------------------------------ launcher
info "Creating launcher script..."
cat > "$INSTALL_DIR/${APP}" << 'SCRIPT'
#!/usr/bin/env bash
SCRIPT="$(readlink -f "$0")"
DIR="$(dirname "$SCRIPT")"
source "$DIR/.venv/bin/activate"
cd "$DIR"
exec python3 -m src
SCRIPT
chmod +x "$INSTALL_DIR/${APP}"
ln -sf "$INSTALL_DIR/${APP}" "$BIN_LINK"
ok "Launcher created at ${BIN_LINK}"

# ------------------------------------------------------------------ desktop
info "Creating desktop entry..."
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_FILE" << DESKTOP
[Desktop Entry]
Name=Rsync GUI
Comment=Graphical interface for rsync
Exec=${BIN_LINK}
Icon=${APP}
Terminal=false
Type=Application
Categories=Utility;FileTransfer;
StartupNotify=true
DESKTOP
ok "Desktop entry created"

# ------------------------------------------------------------------ icon
info "Installing icon..."
mkdir -p "$ICON_DIR"
if [ -f "${SRC_DIR}/icons/${APP}.svg" ]; then
    cp "${SRC_DIR}/icons/${APP}.svg" "$ICON_FILE"
    ok "Icon installed"
else
    info "No icon found, skipping"
fi

# --------------------------------------------------------------- refresh
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$DESKTOP_DIR" &>/dev/null || true
fi
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache /usr/local/share/icons/hicolor/ &>/dev/null || true
fi

echo ""
ok "Installation complete! Run: ${APP}"
