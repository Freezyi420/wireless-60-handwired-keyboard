# Layout verification

Checked on 13 November 2026.

## References and distinction

The [MakerWorld 557186 page](https://makerworld.com/en/models/557186-60-keyboard-with-arrow-keys) is by HappyMangoStudios3D. Its description explicitly links [kanefron5/keyboard-manual](https://github.com/kanefron5/keyboard-manual) as an assembly guide. That guide is a contributor's implementation; it is not a separate firmware repository by the original designer. No independent original-designer keymap was identified on the model page. The public base layer therefore matches the concrete, designer-linked reference rather than claiming access to an unpublished original firmware.

The reference snapshot is commit [`3cecddd2cddfcddb54bceba12389503fe30a3832`](https://github.com/kanefron5/keyboard-manual/tree/3cecddd2cddfcddb54bceba12389503fe30a3832):

- [README: layout `64_ansi` and assembly instructions](https://github.com/kanefron5/keyboard-manual/blob/3cecddd2cddfcddb54bceba12389503fe30a3832/README.md).
- [Physical positions in `keyboard.json`](https://github.com/kanefron5/keyboard-manual/blob/3cecddd2cddfcddb54bceba12389503fe30a3832/roman_keyboard/keyboard.json).
- [Default key assignments](https://github.com/kanefron5/keyboard-manual/blob/3cecddd2cddfcddb54bceba12389503fe30a3832/roman_keyboard/keymaps/default/keymap.c).

The layout has 14 + 14 + 13 + 14 + 9 = 64 keys. The Enter key is horizontal, and the backslash position is on the Q row: this is an ANSI-derived layout, not ISO.

## Changes from the personal firmware

Source: [Freezyi420/zmk-config at `71a05aace51329212815df1d3792cff5ea3402ee`](https://github.com/Freezyi420/zmk-config/tree/71a05aace51329212815df1d3792cff5ea3402ee).

| Position (zero-based) | Scan coordinate | Personal assignment | Public assignment | Reason |
| --- | --- | --- | --- | --- |
| 27, after `]` | R3 C0 / S37 | `NUBS` | `BSLH` | Reference uses ANSI backslash, not ISO non-US backslash |
| 52, between `/` and Up | R1 C2 / S12 | `RSHFT` | `GRAVE` | Reference uses grave/tilde in this position |

All other base assignments match the reference, including GUI/Command, Alt/Option and the dedicated arrows. The Fn layer is preserved exactly from the personal firmware, including F1–F12, Bluetooth profile selection 0–4, selected-profile clear, USB output and BLE output. It intentionally does not copy the reference QMK lighting controls.

The public name is `Handwired60` rather than the personal name. The two experimental Bluetooth/passkey overrides were removed, leaving ZMK v0.3 defaults. Idle and sleep timings are preserved.

## Matrix orientation

Read the keymap from the top left, left to right, then downward. The scan transform deliberately reverses the electrical row/column orientation of the personal build. It starts at R4 C13 (top-left Esc), not R0 C0. The GPIO list and 64 scan coordinates are unchanged from the working source.

The contributor's QMK pin numbers and matrix orientation must not be copied into this nRF52840 build. Only its physical key order, geometry and base assignments are used as layout evidence.

The old editor JSON used visual row/column indices, which disagreed with the actual scan transform. The public JSON is corrected to real scan coordinates. All 64 physical attributes are now present in the DTS layout. The four-key fallback keymap is replaced by an include of the canonical configuration, and the template Studio capability and example URL are removed.
