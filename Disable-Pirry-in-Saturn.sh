#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -e
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
exec >>"$HERE/Pirry-Install.log" 2>&1
date
python3 /storage/.config/yabasanshiro-pirry/integrate.py disable
sync
echo 'Saturn menu integration disabled. Restart ROCKNIX normally.'
