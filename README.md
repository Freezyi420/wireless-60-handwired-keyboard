# Wireless 60% handwired keyboard — ZMK

[![Build ZMK firmware](https://github.com/Freezyi420/wireless-60-handwired-keyboard/actions/workflows/build.yml/badge.svg)](https://github.com/Freezyi420/wireless-60-handwired-keyboard/actions/workflows/build.yml)

Public firmware for a **64-key ANSI keyboard with arrow keys**, based on [MakerWorld model 557186 by HappyMangoStudios3D](https://makerworld.com/en/models/557186-60-keyboard-with-arrow-keys). This variant uses a SuperMini nRF52840 controller, a battery and ZMK for USB/Bluetooth operation.

## Hardware and scope

| Item | This configuration |
| --- | --- |
| Keys | 64, handwired; 5 × 14 scan matrix, 6 unused positions |
| Controller | SuperMini nRF52840, built using ZMK target `nice_nano_v2` |
| Shield | `handwired60` |
| Diodes | `col2row` — cathode/stripe toward the row |
| Connections | USB and Bluetooth LE; five selectable host profiles |
| Power switch | Battery positive → switch → board B+; battery negative → board B− |
| Sleep | Idle at 3 minutes; deep sleep at 30 minutes |
| Firmware | ZMK v0.3, pinned to release commit `edf5c0814fd3ea202e43aad2d68fd32e882a518c` |

The GPIO mapping matches the working personal build. A SuperMini is **not** a Raspberry Pi Pico/RP2040: do not use the Pico pin numbers from the original assembly guide. See [wiring](docs/wiring.md) before soldering. Confirm your board's actual pad labels and pinout; a Pro Micro shape alone does not establish compatibility.
Attention, la pi Pico utilisé par le créateur original ne possède pas de module bluetooth. 

J'ai utilisé la super mini car il s'agit d'une copie low-cost de la Nice Nano V2. D'après ce guide "https://github.com/joric/nrfmicro/wiki/Alternatives", il est déconseillé d'utiliser une copie car ces dernières peuvent poser des soucis dans le temps à cause de composants peu fiable. La copie est cependant bien détecté comme une Nice Nano V2 et est parfaitement compatible. J'ai pris ce risque car la copie coute autour des 8€ contre 25€ pour une vrai Nice Nano V2

The modified case with switch opening, controller holder, photos and 3MF files are not included yet. This repository currently documents the firmware and electrical configuration, rather than a complete illustrated mechanical build.

## Build and install

1. Open **[Actions → Build ZMK firmware](https://github.com/Freezyi420/wireless-60-handwired-keyboard/actions/workflows/build.yml)**. Choose a successful run on `main`, or choose **Run workflow** to build it. If using your own fork, enable Actions first.
2. Download the **firmware** artifact and unzip it.
3. Put the nRF52840 board in its UF2 bootloader, normally by briefly connecting **RST to GND twice** (la carte low-cost est parfois capricieuse pour passer en boot mode il faut parfait persévérer plusieurs fois. Elle clignotera avec sa led rouge quand le boot loader sera actif. Use a data-capable USB cable and check the instructions for your exact board revision.
4. Copy **`handwired60-nice_nano_v2.uf2`** to the bootloader drive. The board reboots automatically.
5. Test all 64 keys over USB, then pair over Bluetooth as described below.

`settings-reset-nice_nano_v2.uf2` is a separate recovery image that erases saved settings, including Bluetooth bonds. **It is not the keyboard firmware.** After using it, enter the bootloader again, flash the normal keyboard image and remove the old device from the host's Bluetooth settings before re-pairing.
Il peut être utile de réinitialiser la puce grâce à ce fichier surtout car flasher un nouveau firmware n'affecte pas les paramètres bluetooth (clés etc) de la carte. Grâce à cette procédure vous pourrez donc repartir de zéro.  

For local build commands and troubleshooting, see [compilation and flashing](docs/build.md).

## Public keymap

The physical arrangement is **ANSI-derived 64-key**, not ISO. Keycodes use the US layout; the operating system's selected input language determines the characters you type.

```text
Esc  1  2  3  4  5  6  7  8  9  0  -  =  Backspace
Tab   Q  W  E  R  T  Y  U  I  O  P  [  ]  \
Caps   A  S  D  F  G  H  J  K  L  ;  '     Enter
Shift   Z  X  C  V  B  N  M  ,  .  /  `  Up  Delete
Ctrl GUI Alt       Space       RAlt Fn Left Down Right
```

This follows the base layer in the assembly guide linked by the MakerWorld designer. In particular, the key after `]` sends **backslash**, and the key between `/` and Up sends **grave/tilde**. There is no dedicated right Shift in that reference layout. On macOS, GUI is Command and Alt is Option. See [layout verification and changes](docs/layout.md) for source links and the exact differences from the personal firmware.

Hold **Fn** to use the secondary layer:

| Combination | Action |
| --- | --- |
| Fn + 1 … 0, −, = | F1 … F12 |
| Fn + Q / W / E / R / T | Select Bluetooth profile 1 / 2 / 3 / 4 / 5 (internal indices 0–4) |
| Fn + Backspace | Clear the currently selected Bluetooth profile |
| Fn + Enter | Prefer Bluetooth output |
| Fn + Space | Prefer USB output |

All other Fn positions are transparent, preserving base modifiers and arrows. Fn is momentary: release it to return to the base layer.

## Pairing with Windows, macOS or Linux

1. Power on the keyboard and select an unused profile with **Fn + Q/W/E/R/T**.
2. Choose **Fn + Enter** if USB is attached but you want to type over Bluetooth.
3. In the host's Bluetooth settings, pair with **Handwired60**.
4. To replace the host in a profile, select that profile, press **Fn + Backspace**, forget the old keyboard entry on the host and pair again. This command clears only the selected profile.

The public configuration uses ZMK's default Bluetooth pairing settings. It does not enable experimental security or passkey entry and has no Linux/Omarchy-specific overrides. This is a configuration choice, not evidence of physical testing on every OS. USB can still supply power while BLE is selected; the power switch disconnects the battery, not USB power. See the official [Bluetooth behavior documentation](https://zmk.dev/docs/keymaps/behaviors/bluetooth) and [output selection documentation](https://zmk.dev/docs/keymaps/behaviors/outputs).

## Editing and checking

- `config/handwired60.keymap` is the canonical keymap. The shield fallback includes the same file.
- `config/handwired60.conf` contains the public name and power settings.
- `boards/shields/handwired60/handwired60.overlay` defines the GPIOs and scan transform.
- `handwired60-layouts.dtsi` contains all 64 physical positions; `config/handwired60.json` uses the same real scan coordinates.
- ZMK Studio is not advertised or enabled.

Run `python3 scripts/check_config.py` before publishing changes. CI checks the configuration and compiles both the keyboard and settings-reset images. A successful compilation still requires a physical key-by-key and host-pairing test after flashing.

## Credits and provenance

- [HappyMangoStudios3D's original model](https://makerworld.com/en/models/557186-60-keyboard-with-arrow-keys).
- [Roman Zabolotskikh / kanefron5's assembly guide](https://github.com/kanefron5/keyboard-manual), linked by the original designer, including its 64-key layout reference.
- [ZMK firmware](https://github.com/zmkfirmware/zmk/tree/edf5c0814fd3ea202e43aad2d68fd32e882a518c).
- [nRFMicro Wiki — Alternatives](https://github.com/joric/nrfmicro/wiki/Alternatives), comparison of nice!nano-compatible boards and lower-cost alternatives such as the SuperMini nRF52840. 

The original 3D models and third-party material retain their own terms. They are linked, not redistributed or relicensed here.
