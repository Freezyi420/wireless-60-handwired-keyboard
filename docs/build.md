# Building and flashing

## GitHub Actions (recommended)

The repository's [Build ZMK firmware workflow](https://github.com/Freezyi420/wireless-60-handwired-keyboard/actions/workflows/build.yml) runs on pushes, pull requests and manual dispatch. It validates the 64-key configuration before calling ZMK's reusable build workflow. Both the firmware and the reusable workflow are fixed to the ZMK v0.3 release commit, `edf5c0814fd3ea202e43aad2d68fd32e882a518c`.

`build.yaml` defines two independent builds:

| Board | Shield | Output |
| --- | --- | --- |
| `nice_nano_v2` | `handwired60` | `handwired60-nice_nano_v2.uf2` |
| `nice_nano_v2` | `settings_reset` | `settings-reset-nice_nano_v2.uf2` |

Wait until the entire run is successful, then download and unzip the merged **firmware** artifact. GitHub may require you to sign in to download artifacts. A fork may require enabling Actions first. No secrets are required for compilation.

The board target is retained from the owner's working SuperMini nRF52840 build. Do not select an RP2040 target even though the original mechanical model used a Pico.

## Local build

Install the native dependencies, Zephyr SDK and `west` using the [official ZMK setup guide](https://zmk.dev/docs/development/local-toolchain/setup/native), or use the [official container environment](https://zmk.dev/docs/development/local-toolchain/setup/container). These commands assume a working ZMK v0.3-compatible toolchain; they do not install it. Use a new workspace outside any existing west workspace.

```sh
git clone https://github.com/Freezyi420/wireless-60-handwired-keyboard.git
cd wireless-60-handwired-keyboard
python3 scripts/check_config.py
cd ..
mkdir handwired60-build
cd handwired60-build
cp -R ../wireless-60-handwired-keyboard/config ./config
west init -l config
west update
west zephyr-export
python3 -m pip install -r zephyr/scripts/requirements.txt
```

From `handwired60-build`, build the keyboard:

```sh
west build -p always -s zmk/app -d build/keyboard -b nice_nano_v2 -- \
  -DSHIELD=handwired60 \
  -DZMK_CONFIG="$(realpath ../wireless-60-handwired-keyboard/config)" \
  -DZMK_EXTRA_MODULES="$(realpath ../wireless-60-handwired-keyboard)"
```

Build the recovery image separately:

```sh
west build -p always -s zmk/app -d build/settings-reset -b nice_nano_v2 -- \
  -DSHIELD=settings_reset \
  -DZMK_CONFIG="$(realpath ../wireless-60-handwired-keyboard/config)" \
  -DZMK_EXTRA_MODULES="$(realpath ../wireless-60-handwired-keyboard)"
```

The results are `build/keyboard/zephyr/zmk.uf2` and `build/settings-reset/zephyr/zmk.uf2`. Keep the filenames distinct when copying them elsewhere. These examples use a POSIX shell with `realpath`; on Windows use the official container environment or supply absolute paths appropriate to your shell.

The root `zephyr/module.yml` registers the custom board root. `ZMK_EXTRA_MODULES` must point to the repository root, not just `config/`. The official reusable workflow supplies it automatically.

## Flash and test

1. Connect using a USB data cable.
2. Enter the UF2 bootloader using the board's documented reset procedure (typically two brief RST–GND connections).
3. Copy the **keyboard** image to its USB mass-storage drive. It should reboot automatically.
4. Verify all 64 physical positions, including backslash, grave, arrows, modifiers, Fn and F1–F12. Test symbols with a US host layout first to separate firmware mapping from OS language settings.
5. Pair each desired Bluetooth host. Test switching profiles, clearing only the selected profile, and USB/BLE output selection. Verify sleep and wake.

No flashing is performed by the workflow. A compile result cannot prove the physical wiring or Windows/macOS interoperability; those need a keyboard and hosts.

## Recovery

If an old bond prevents pairing, first select that profile and press **Fn + Backspace**; also remove the keyboard on the host. If necessary, flash the **settings reset** image, then enter the bootloader again and flash the keyboard image. This erases all stored ZMK settings; all hosts need to be paired again. A normal firmware flash does not automatically erase bonds.

If there is no UF2 drive, check the cable and exact board bootloader instructions. Do not follow the Pico BOOTSEL/QMK instructions from the original mechanical build.

If compilation reports an unknown shield, check the repository's `zephyr/module.yml`, the `ZMK_EXTRA_MODULES` root path and the exact name `handwired60`. For layout errors, run the configuration check and inspect `build/keyboard/zephyr/zephyr.dts` and `.config`. The GitHub workflow also prints the generated devicetree and Kconfig files in its job logs.
