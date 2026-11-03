## Pirry Complete for RG ARC-D — first public beta

One installer for the original Pirry 1.6.2 emulator, ARC controls and a native Saturn emulator choice on ROCKNIX.

### Targets

- Anbernic **RG ARC-D**.
- Official ROCKNIX **20261101** (main documented setup) or **20261001**.
- Original upstream **Pirry v1.6.2**, downloaded from its author and checksum-verified.

### Install

Download **Pirry-Complete-1.6.2-ARC-D.zip** from this release's assets. Extract into the games card's `ports` folder, connect to Wi-Fi, refresh game lists, and run **Install-Saturn-Pirry**. Restart ROCKNIX, then choose **pirry** in Saturn's system emulator settings.

The complete package includes the InputPlumber controller fix and normal Saturn menu integration. No older separate packages or per-game Ports shortcuts are required.

### Notes

Saves and existing artwork are retained. The installer pins 1.6.2 rather than automatically fetching future upstream releases. No games, BIOS, artwork or emulator executable are bundled.

The original emulator and updated controller helper were confirmed working on the user's ARC-D. Combined installation tests passed locally for both firmware targets with hardware execution mocked; a full independent fresh-device test is still needed. This initial integration release is therefore marked **beta**.

### Credits

Pirry: pirrypirrypirry. Yaba Sanshiro: devMiyax. Yabause and ROCKNIX: their respective contributors. This is an unofficial integration; the upstream emulator code is unchanged.
