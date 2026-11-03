# Credits and source references

This repository packages a community integration of an existing emulator into ROCKNIX. It does not claim authorship of the emulator or affiliation with the upstream projects.

| Contribution | Project / source |
|---|---|
| Pirry emulator optimizations and release | [pirrypirrypirry/yabasanshiro-pirry](https://github.com/pirrypirrypirry/yabasanshiro-pirry) and [release repository](https://github.com/pirrypirrypirry/yabasanshiro-pirry-release) |
| Yaba Sanshiro | [devMiyax/yabause](https://github.com/devmiyax/yabause) |
| Original Yabause work | Yabause contributors; upstream license and notices apply |
| Firmware and launch framework | [ROCKNIX/distribution](https://github.com/ROCKNIX/distribution) |
| Original launch-script copyright notices | Shanti Gilbert, JELOS and applicable ROCKNIX contributors; retained in the generated private runner |
| Raw ARC controller mapping | [ROCKNIX 20261001 ARC mapping](https://github.com/ROCKNIX/distribution/blob/20261001/projects/ROCKNIX/packages/emulators/standalone/yabasanshiro-sa/config/devices/keymapv2_rg_arc_joypad.json) |
| InputPlumber ARC-D mapping | [ROCKNIX 20261101 ARC-D mapping](https://github.com/ROCKNIX/distribution/blob/20261101/projects/ROCKNIX/packages/emulators/standalone/yabasanshiro-sa/config/devices/keymapv2_Anbernic%20RG%20ARC-D.json) |
| Virtual controller definition | [ROCKNIX 20261101 ARC InputPlumber profile](https://github.com/ROCKNIX/distribution/blob/20261101/projects/ROCKNIX/devices/RK3566/filesystem/usr/share/inputplumber/devices/01-rg-arc.yaml) |
| Additional system/emulator command support | [ROCKNIX/emulationstation-next](https://github.com/ROCKNIX/emulationstation-next) |

The integration scripts were assembled with ChatGPT assistance and tested through a user troubleshooting session. See the setup guide for the exact limits of testing.

Integration scripts are marked GPL-2.0-or-later; the GPL version 2 text is included in `LICENSE`. Preserve upstream copyright and license notices when sharing or modifying the files.

The downloaded Pirry executable remains the original upstream artifact. Its source and applicable notices are maintained in the upstream repositories linked above. No modified emulator executable is distributed in this repository.
