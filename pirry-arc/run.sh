#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -e
BASE=$(cd -- "$(dirname -- "$0")" && pwd)
LOG="$BASE/last-launch.log"
exec >>"$LOG" 2>&1
date
echo 'Pirry 1.6.3 / ROCKNIX / RG ARC-D'
fail() { echo "FAILED: $*"; exit 1; }
[[ $(uname -m) == aarch64 ]] || fail 'An aarch64 handheld is required.'
[[ -f /etc/os-release ]] && cat /etc/os-release
[[ -f /proc/device-tree/model ]] && tr -d '\0' </proc/device-tree/model
echo
# Keep a legacy private library path for backups of the older emulator.
if [[ -d "$BASE/lib" ]]; then
    export LD_LIBRARY_PATH="$BASE/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
LOADER=/lib/ld-linux-aarch64.so.1
[[ -x "$LOADER" ]] || fail "Missing native loader: $LOADER"
[[ -x "$BASE/yabasanshiro-pirry" ]] || fail 'Run Install Saturn Pirry first.'
"$LOADER" --list "$BASE/yabasanshiro-pirry" || fail 'Missing/incompatible library; send this log.'
echo 'Native dependencies resolved.'
if [[ ${1:-} == --check ]]; then
    echo 'Dependency check only; graphics and audio have not been tested.'
    exit 0
fi
[[ $# == 1 && -f $1 ]] || fail 'Expected one existing Saturn disc or playlist path.'
[[ -n ${HOME:-} && $HOME == /storage* ]] || fail 'Expected ROCKNIX home under /storage.'
command -v python3 >/dev/null || fail 'python3 is required for SDL controller setup.'
python3 "$BASE/prepare-controls.py" "$BASE/arc-keymap.json" || fail 'Controller setup failed.'
# Upstream defaults to unversioned library names, absent on some runtime images.
export SDL_VIDEO_EGL_DRIVER=libEGL.so.1
export SDL_VIDEO_GL_DRIVER=libGLESv2.so.2
# Ports/runemu has already suspended EmulationStation and configured the display.
# Load ROCKNIX hotkey helpers when available, preserving its display/audio variables.
set +e
. /etc/profile
if declare -F set_kill >/dev/null; then set_kill set '-9 yabasanshiro-pirry'; fi
set -e
ARGS=(-r 3 -rr 0 -i "$1")
for bios in saturn_bios.bin sega_101.bin mpr-17933.bin sega1003.bin; do
    if [[ -f /storage/roms/bios/$bios ]]; then
        ARGS+=(-b "/storage/roms/bios/$bios")
        break
    fi
done
echo "Launching: $1"
cd -- "$BASE"
set +e
"$BASE/yabasanshiro-pirry" "${ARGS[@]}"
status=$?
echo "Emulator exit status: $status"
exit "$status"
