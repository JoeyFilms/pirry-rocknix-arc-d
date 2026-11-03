# Pirry Complete for ROCKNIX on RG ARC-D

Install **Pirry 1.6.2** into the normal **Saturn** section on the **Anbernic RG ARC-D** with one installer. Keep the usual Saturn game entries, box art, descriptions and favourites—no per-game Ports shortcuts or separate controller patches are needed.

This is an **unofficial ROCKNIX integration**, not a new emulator fork. It downloads the original emulator from [pirrypirrypirry's release](https://github.com/pirrypirrypirry/yabasanshiro-pirry-release/releases/tag/v1.6.2).

**[Download the complete installer ZIP](https://github.com/JoeyFilms/pirry-rocknix-arc-d/raw/refs/heads/main/downloads/Pirry-Complete-1.6.2-ARC-D.zip)** · **[Detailed setup guide](docs/SETUP.md)** · **[Troubleshooting](docs/SETUP.md#troubleshooting)**

## Compatibility

| Item | Supported target |
|---|---|
| Handheld | **Anbernic RG ARC-D** |
| Main documented firmware | **Official ROCKNIX 20261101**, RK3566 aarch64 Generic image |
| Also supported by the installer | Official ROCKNIX **20261001** |
| Emulator downloaded | Original **Pirry v1.6.2**, ARM64/dArkOS release |
| Controls | Old raw ARC controls and 20261101's InputPlumber virtual controller |
| Other hardware / firmware | Not validated; installer refuses other device/version targets |

If ROCKNIX 20261101 already works on your ARC-D, you do not need to reflash it. The [full guide](docs/SETUP.md#1-check-your-rocknix-version) explains the exact image and fresh-firmware prerequisites.

## Quick install

1. Download the installer ZIP linked above and extract its contents into the games card's existing **`ports`** folder.
2. Connect the ARC-D to Wi-Fi and open **START → Game Settings → Update Gamelists**.
3. Open **Ports → Install-Saturn-Pirry**. Wait for it to return to the menu.
4. Restart ROCKNIX normally.
5. Open **START → Game Settings → Per System Advanced Configuration → Saturn**. Select **Emulator: `pirry`** and **Core: `pirry`**, if shown.
6. Launch games directly from **Saturn**.

The installer downloads approximately 5 MB, verifies it, installs the correct controller support and adds the emulator choice. The included **Disable-Pirry-in-Saturn** entry is optional; it is not another installation step.

You need **only this complete package**. Do not install the old menu add-on or controller-repair packages afterward.

## What is included

- Verified upstream emulator download, pinned to 1.6.2.
- ARC six-button mappings for both supported firmware controller interfaces.
- Automatic backup and mapping migration when the interface changes.
- Saturn-only emulator integration, retaining the original emulator choices.
- Private launch wrapper based on the installed ROCKNIX launcher.
- Clear installation logs and an optional disable action.

No games, BIOS, artwork, personal saves or login credentials are included. The emulator executable is downloaded from its author rather than bundled here. Existing saves and game metadata are retained.

## Updates and test status

Rerunning this installer **does not fetch the newest upstream release**. It keeps or installs verified **1.6.2**. Supporting another emulator/firmware release requires an explicit package update and compatibility checks.

The original Pirry installation and controller repair were confirmed working during ARC-D testing. The combined installer passed local simulated installation tests for both firmware versions. Its first complete fresh-device installation still needs confirmation: treat the initial public release as a **beta** and report the exact firmware and log if something fails.

## More information

- [Full installation, artwork, controls and troubleshooting guide](docs/SETUP.md)
- [Beginner's guide to publishing this project on GitHub](docs/GITHUB-PUBLISHING.md)
- [Release notes](CHANGELOG.md)
- [Credits and source references](CREDITS.md)
- [License](LICENSE)

## Credits

**Pirry emulator:** [pirrypirrypirry](https://github.com/pirrypirrypirry/yabasanshiro-pirry-release), based on **Yaba Sanshiro** by **devMiyax** and the **Yabause** project. ROCKNIX's contributors provide the firmware, controller mappings and launch framework used by this integration. See [CREDITS.md](CREDITS.md).
