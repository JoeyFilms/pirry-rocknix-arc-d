#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Complete installer 1.1: original Pirry 1.6.3, ARC controls and native Saturn entry.
set -e
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
LOG="$HERE/Pirry-Install.log"
DEST=/storage/.config/yabasanshiro-pirry
exec >>"$LOG" 2>&1
trap 'rc=$?; echo "FAILED at line $LINENO (exit $rc): $BASH_COMMAND"; sync; exit "$rc"' ERR
fail() { echo "FAILED: $*"; sync; exit 1; }
date
echo 'Pirry Complete installer 1.1 / emulator 1.6.3'
[[ $(uname -m) == aarch64 ]] || fail 'Run this on an aarch64 RG ARC-D.'
cat /etc/os-release
grep -qi ROCKNIX /etc/os-release || fail 'ROCKNIX required.'
grep -Eq '^(OS_VERSION|VERSION_ID)="?(20261001|20261101)"?$' /etc/os-release || fail 'Supported firmware: official ROCKNIX 20261001 or 20261101.'
model=$(tr -d '\0' </proc/device-tree/model)
echo "Device: $model"
[[ $model == *'RG ARC-D'* ]] || fail 'This package targets RG ARC-D only.'
command -v python3 >/dev/null || fail 'python3 is required.'
[[ -x /lib/ld-linux-aarch64.so.1 ]] || fail 'Native aarch64 dynamic loader is missing.'
FILES=(run.sh prepare-controls.py arc-keymap.json arc-keymap-inputplumber.json integrate.py)
for file in "${FILES[@]}"; do
    [[ -s "$HERE/pirry-arc/$file" ]] || fail "Missing package file: pirry-arc/$file. Extract the complete ZIP."
done
mkdir -p "$DEST"
echo '[1/5] Getting and verifying the emulator'
BIN="$DEST/yabasanshiro-pirry"
EXPECTED=d552c99b224413eb661c4b5b7eb0865e0f0096c2110c47b6cfdec4095b6f4715
verify() { [[ -f $1 ]] && [[ $(sha256sum "$1" | cut -d' ' -f1) == "$EXPECTED" ]]; }
if ! verify "$BIN"; then
    if verify "$HERE/yabasanshiro-pirry"; then
        cp "$HERE/yabasanshiro-pirry" "$BIN.download"
    else
        command -v curl >/dev/null || fail 'curl is missing. See README for offline installation.'
        echo 'Downloading the original GitHub v1.6.3 release (about 5 MB).'
        curl --fail --location --retry 2 --connect-timeout 20 --max-time 180 \
          https://github.com/pirrypirrypirry/yabasanshiro-pirry-release/releases/download/v1.6.3_dArkOS/yabasanshiro-pirry \
          -o "$BIN.download"
    fi
    verify "$BIN.download" || fail 'Downloaded emulator checksum mismatch; previous executable preserved.'
    chmod +x "$BIN.download"
    /lib/ld-linux-aarch64.so.1 --list "$BIN.download" || fail 'New emulator dependencies unresolved; previous executable preserved.'
    if [[ -s "$BIN" ]]; then
        previous=$(mktemp "$BIN.previous-XXXXXX")
        cp -p "$BIN" "$previous"
        cmp -s "$BIN" "$previous" || fail 'Previous emulator backup check failed.'
        echo "Previous executable saved: $previous"
    fi
    sync
    mv "$BIN.download" "$BIN"
else
    echo 'Verified 1.6.3 already installed; keeping it.'
fi
chmod +x "$BIN"
echo '[2/5] Installing the combined launcher and controller helpers'
for file in "${FILES[@]}"; do
    if [[ -f "$DEST/$file" ]] && ! cmp -s "$HERE/pirry-arc/$file" "$DEST/$file"; then
        previous=$(mktemp "$DEST/$file.previous-XXXXXX")
        cp -p "$DEST/$file" "$previous"
        cmp -s "$DEST/$file" "$previous" || fail "Backup check failed: $file"
    fi
    cp "$HERE/pirry-arc/$file" "$DEST/$file.new"
    cmp -s "$HERE/pirry-arc/$file" "$DEST/$file.new" || fail "Copy check failed: $file"
    mv "$DEST/$file.new" "$DEST/$file"
done
chmod +x "$DEST/run.sh"
sync
echo '[3/5] Checking native dependencies'
if ! bash "$DEST/run.sh" --check; then
    cat "$DEST/last-launch.log" 2>/dev/null || true
    fail 'Dependency check failed. Send Pirry-Install.log from ports.'
fi
echo '[4/5] Preparing the matching ARC controller layout'
python3 "$DEST/prepare-controls.py" "$DEST/arc-keymap.json" || fail 'Controller preparation failed. See details above; disconnect external controllers and retry if ambiguous.'
echo '[5/5] Adding Pirry to the original Saturn emulator list'
python3 "$DEST/integrate.py" enable || fail 'Emulator installed, but Saturn menu integration failed. Existing custom configurations are preserved; see details above.'
printf '%s\n' '1.6.3' > "$DEST/installed-version.txt"
sync
echo 'SUCCESS: Emulator, controller support and native Saturn integration installed.'
echo 'Restart ROCKNIX normally, then START > Game Settings > Per System Advanced Configuration > Saturn.'
echo 'Choose emulator pirry (and core pirry if shown). Launch games from the normal Saturn section.'
echo 'No per-game Ports shortcuts are needed. Existing shortcuts remain usable.'
echo "Install log: $LOG"
