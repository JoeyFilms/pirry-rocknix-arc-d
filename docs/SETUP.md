# Detailed setup: Pirry Complete on RG ARC-D

This guide installs the original **Pirry 1.6.3** emulator, the correct ARC controller support and a selectable **pirry** entry inside ROCKNIX's normal **Saturn** section. It is a single installation: no separate menu patch, controller repair or SSH session is required.

## 1. Check your ROCKNIX version

**For a new setup, use official ROCKNIX 20261101 for RK3566 aarch64, Generic.** The installer also supports official **20261001**. Do not choose a different/newer version on the assumption that it will work: controller and launch behaviour changed between these two releases, and the installer intentionally checks versions.

| Handheld | Firmware target | Notes |
|---|---|---|
| RG ARC-D | **20261101** | Main path in this guide; includes InputPlumber controller support |
| RG ARC-D | **20261001** | Also accepted; uses the older ARC controller interface |
| RG ARC-S | Not validated | Installer targets ARC-D only |
| Other devices or firmware | Not validated | Installer stops instead of making unsupported changes |

On the handheld, use **START → System Settings → System Information** if available to check the version. The installer also writes the detected version to `Pirry-Install.log` in the `ports` folder.

For 20261101, the exact system image is:

```text
ROCKNIX-RK3566.aarch64-20261101-Generic.img.gz
```

- [Download that exact image](https://github.com/ROCKNIX/distribution/releases/download/20261101/ROCKNIX-RK3566.aarch64-20261101-Generic.img.gz)
- [Official 20261101 release page](https://github.com/ROCKNIX/distribution/releases/tag/20261101)
- [Official ARC device guide](https://rocknix.org/devices/anbernic/rgarc/)
- [Official ROCKNIX installation guide](https://rocknix.org/play/install/)

**Already running a supported ROCKNIX version? Skip firmware installation.** This add-on does not need you to format a card or erase Android.

**Starting from the stock Anbernic software?** Follow the official ARC-specific instructions before this guide. Installing ROCKNIX on ARC-D has Android/eMMC boot requirements, and the official procedure warns that Android may be erased. Back up anything you want to keep. To install the system image, decompress it and write it to the operating-system card using the official imaging procedure; do not merely copy the image file onto a card. Choose the correct target card because flashing overwrites it.

This integration package does not flash ROCKNIX or perform those device changes.

## 2. Get the complete Pirry installer

Download **`Pirry-Complete-1.6.3-ARC-D.zip`** from this project's download link or release assets. The installer ZIP is the file intended for the handheld; a GitHub-generated source-code archive is the project source and has a different directory layout.

You also need:

- An ARC-D with supported ROCKNIX already booting correctly.
- Wi-Fi for the approximately 5 MB emulator download, unless using the offline option below.
- Your own Saturn game dumps, preferably a CHD for the first test.
- A way to copy files to the games card or its normal `roms` network share.

Keep a backup of existing saves before changing emulator setups. No ROMs or BIOS files are provided by this project.

## 3. Copy the installer to the correct folder

For a two-card setup, shut down the ARC normally before removing the **games card**. Open that card on your computer and find its existing `roms` folder, then `ports`. Use the same folder ROCKNIX already uses for Ports.

On Windows, right-click the downloaded ZIP and choose **Extract All**. Open the extracted folder and copy its **contents** into `ports`. Do not copy the still-zipped file, and do not leave the installer inside an extra enclosing `Pirry-Complete-...` folder.

The important files should be at these relative locations:

| File | Location on the games card |
|---|---|
| Installer | `roms/ports/Install-Saturn-Pirry.sh` |
| Optional disable entry | `roms/ports/Disable-Pirry-in-Saturn.sh` |
| Main launcher | `roms/ports/pirry-arc/run.sh` |
| Controller helper | `roms/ports/pirry-arc/prepare-controls.py` |
| New controller template | `roms/ports/pirry-arc/arc-keymap-inputplumber.json` |
| Menu integration helper | `roms/ports/pirry-arc/integrate.py` |

If Windows assigns the games card drive letter `X:`, for example, the installer is `X:\roms\ports\Install-Saturn-Pirry.sh`. The actual drive letter will vary.

When using the network share, open its `roms` directory and use the same existing `ports` folder. For other ROCKNIX storage layouts, follow the [official file-transfer guide](https://rocknix.org/play/add-games/) rather than creating a second unused `ports` directory.

Do not rename `.sh` files to `.txt` or edit them in Word. Safely eject the card, insert it into the ARC-D while powered off, and boot ROCKNIX.

## 4. Put games and optional BIOS files in their normal places

Keep Saturn games in the existing `saturn` folder. For a first test, use a CHD or a properly paired CUE/BIN dump. Do not put Saturn games inside `ports`.

For the two-card layout used during testing:

| Content | Games-card location | Runtime path on ROCKNIX |
|---|---|---|
| Saturn games | `roms/saturn/` | `/storage/roms/saturn/` |
| BIOS files | `roms/bios/` | `/storage/roms/bios/` |
| Installer | `roms/ports/` | `/storage/roms/ports/` |

The external card may physically mount at `/storage/games-external/roms/`; ROCKNIX presents the normal `/storage/roms/` game path to the frontend. You do not need to change the game paths manually.

The Pirry wrapper can find these optional BIOS filenames directly inside the normal BIOS directory:

- `saturn_bios.bin`
- `sega_101.bin`
- `mpr-17933.bin`
- `sega1003.bin`

Use BIOS files you have obtained yourself. The wrapper uses the first matching file in that order. Without one, it launches the emulator's BIOS emulation. This wrapper's BIOS choice is separate from the stock emulator's **Use HLE BIOS** setting.

## 5. Run the one installer

1. On the ARC-D, connect to Wi-Fi through **START → Network Settings**.
2. For the initial controller test, disconnect external controllers.
3. Press **START → Game Settings → Update Gamelists**. Confirm if asked.
4. Open **Ports**.
5. Select **Install-Saturn-Pirry**.
6. Wait until it returns to the menu. Do not switch off the handheld during installation.

The installer performs five stages: verifies/downloads 1.6.3, installs helpers, checks dependencies, prepares the matching controls, and adds the normal Saturn emulator entry. It logs progress to **`Pirry-Install.log` directly in `ports`**. If the entry returns immediately or the next steps fail, read that log before reinstalling repeatedly.

You do not need to run anything called Enable-Pirry or Repair-Pirry-Controls. Those old separate patches have been incorporated.

## 6. Restart and select Pirry

Restart ROCKNIX through its normal restart menu. A game-list refresh alone may not reload newly added emulator definitions.

After restarting:

1. Open **START → Game Settings → Per System Advanced Configuration → Saturn**.
2. Set **Emulator** to **`pirry`**.
3. If a core selector appears, set **Core** to **`pirry`**.
4. Return to the normal **Saturn** system and launch a game.

A previously selected system emulator can override the automatic default, so select Pirry explicitly once. Individual game overrides also take priority: if one title still uses a stock emulator, set that game's emulator to **Auto** or **pirry**.

For the first launch, start the game normally rather than loading an old save state. Save states made with another emulator/version may be incompatible.

## 7. Controls, artwork and performance

| Action | Control |
|---|---|
| Open Pirry's in-game menu | **Select** |
| Exit the game | **Select + Start** |
| Save/load state | Pirry menu → **Save** submenu |

The helper uses the official ARC six-button layout for the detected interface. On 20261101, SDL can call the built-in controls **Sony Interactive Entertainment DualSense Wireless Controller**. This is expected from InputPlumber; it does not mean a physical PlayStation controller is required.

When moving from the old raw interface to the virtual one, the helper backs up your old controller JSON and selects the matching layout. Custom control changes are retained on subsequent launches on the same interface. Old physical-interface customizations remain in the backup because their button IDs cannot simply be reused.

Games stay in the original Saturn section, so existing artwork, descriptions and favourites remain available. For new artwork, use ROCKNIX's normal [scraping tools](https://rocknix.org/configure/scraper/). This installer does not download artwork itself.

Pirry has a global sound DSP setting. If speed or heat worsens, try **DSP Off** in Pirry's sound menu. Resolution and aspect ratio are also configured in Pirry; not every stock emulator option is connected to this wrapper.

First establish that ordinary ROCKNIX games run reliably. An ARC-D in our troubleshooting session hard-reset under Saturn load until a stable undervolt was configured. ROCKNIX documents three undervolt levels; stability varies by unit. Keep overclock disabled while diagnosing reboots and follow the [official ARC tweaks documentation](https://rocknix.org/devices/anbernic/rgarc/#tweaks). The installer itself changes no voltage or clock settings.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Installer is absent from Ports | Extracted `.sh` and `pirry-arc` folder must be directly in the real `ports` folder; update game lists. |
| Installer returns but no Pirry choice appears | Read `ports/Pirry-Install.log`; confirm supported version; restart normally. |
| Firmware-version refusal | Only 20261001 and 20261101 are targeted. Do not bypass the check for another build. |
| `rg_arc_joypad not found` from an old helper | Use the complete current package; do not reinstall older separate patches afterward. |
| More than one matching controller | Disconnect external controllers and rerun the installer once. |
| Controller JSON parsing error | Keep the error and mapping backup; do not delete all emulator settings or saves. |
| A game still launches the stock emulator | Check that game's emulator override; set Auto or pirry. |
| Missing native library or checksum mismatch | Keep the log. A failed new-download check preserves the previous executable. |
| Conflict with another custom Saturn config | Installer leaves it untouched and names the file. Reconcile it before retrying. |
| Whole device reboots | Treat this as a firmware/thermal/power stability issue, not proof of a Pirry crash. Check stock gameplay too. |

Useful files:

| Purpose | Location |
|---|---|
| Installation progress/errors | `Pirry-Install.log` in the card's `ports` folder |
| Emulator launch log | `/storage/.config/yabasanshiro-pirry/last-launch.log` |
| Program files | `/storage/.config/yabasanshiro-pirry/` |
| Pirry settings and saves | `/storage/.yabasanshiro/` |
| Saturn menu override | `/storage/.config/emulationstation/es_systems_zz_pirry.cfg` |

The launch log appends sessions, so its latest lines are usually the useful part. Do not publish achievements credentials, passwords or private token files with a bug report.

## Updates, old installations and disabling

- This package pins **Pirry 1.6.3**. Running it again does not automatically install a newer GitHub release.
- Reinstallation keeps a matching executable, preserves saved data and refreshes the helpers/menu integration. Changed helpers and older executables are backed up.
- Do not install old separate controller/menu ZIPs afterward; they can replace updated helpers.
- Future ROCKNIX releases need compatibility checking. The installer targets exact versions intentionally.
- To restore the original Saturn choices, run **Ports → Disable-Pirry-in-Saturn**, then restart normally. This disables the menu override without deleting saves or the emulator.
- If your existing installation already works, you do not need to reinstall merely because this combined package exists.

## Offline option

Download the original executable named `yabasanshiro-pirry` from the exact [v1.6.3 dArkOS release](https://github.com/pirrypirrypirry/yabasanshiro-pirry-release/releases/tag/v1.6.3_dArkOS). Put it beside `Install-Saturn-Pirry.sh` and run the same installer. Do not choose the separate ArkOS build.

Expected size: **4,891,960 bytes**. Expected SHA-256:

```text
d552c99b224413eb661c4b5b7eb0865e0f0096c2110c47b6cfdec4095b6f4715
```

## Verification status

Pirry 1.6.2 and the newer controller helper were confirmed working on the ARC-D. The 1.6.3 binary has the same declared shared-library and version requirements. The 1.6.3 installer update was checked locally and still needs gameplay testing on an ARC-D.
