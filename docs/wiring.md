# Wiring for this nRF52840 variant

These are **nRF52840 GPIO names**, not printed Pro Micro pin numbers or the RP2040 GPIOs in the original guide. Taken unchanged from the working personal configuration at commit `71a05aace51329212815df1d3792cff5ea3402ee`.

## GPIO assignments

| Matrix node | nRF52840 GPIO |
| --- | --- |
| C0 | P0.06 |
| C1 | P0.08 |
| C2 | P0.17 |
| C3 | P0.20 |
| C4 | P0.22 |
| C5 | P0.24 |
| C6 | P1.00 |
| C7 | P0.11 |
| C8 | P1.04 |
| C9 | P1.06 |
| C10 | P0.31 |
| C11 | P0.29 |
| C12 | P0.02 |
| C13 | P1.15 |
| R0 | P1.13 |
| R1 | P1.11 |
| R2 | P0.10 |
| R3 | P0.09 |
| R4 | P1.07 |

The scan direction is `col2row`: column → switch → diode → row. The diode cathode (stripe) is on the row side. Columns are active high; rows are active high with pull-downs. P0.09 and P0.10 normally have an NFC function: the overlay enables `nfct-pins-as-gpios` for their use as rows.

## Physical keys → scan coordinates

Front view, reading left to right across each row from top to bottom. `S64` is the top-left Esc key; `S01` is the bottom-right arrow. Electrical row R4 is at the top. Do not reverse the transform to make the numbering look more familiar: it matches the working wiring.

| Keymap index | Switch | Base action | Matrix |
| --- | --- | --- | --- |
| 0 | S64 | `&kp ESC` | R4 C13 |
| 1 | S63 | `&kp N1` | R4 C12 |
| 2 | S62 | `&kp N2` | R4 C11 |
| 3 | S61 | `&kp N3` | R4 C10 |
| 4 | S60 | `&kp N4` | R4 C9 |
| 5 | S59 | `&kp N5` | R4 C8 |
| 6 | S58 | `&kp N6` | R4 C7 |
| 7 | S57 | `&kp N7` | R4 C6 |
| 8 | S56 | `&kp N8` | R4 C5 |
| 9 | S55 | `&kp N9` | R4 C4 |
| 10 | S54 | `&kp N0` | R4 C3 |
| 11 | S53 | `&kp MINUS` | R4 C2 |
| 12 | S52 | `&kp EQUAL` | R4 C1 |
| 13 | S51 | `&kp BSPC` | R4 C0 |
| 14 | S50 | `&kp TAB` | R3 C13 |
| 15 | S49 | `&kp Q` | R3 C12 |
| 16 | S48 | `&kp W` | R3 C11 |
| 17 | S47 | `&kp E` | R3 C10 |
| 18 | S46 | `&kp R` | R3 C9 |
| 19 | S45 | `&kp T` | R3 C8 |
| 20 | S44 | `&kp Y` | R3 C7 |
| 21 | S43 | `&kp U` | R3 C6 |
| 22 | S42 | `&kp I` | R3 C5 |
| 23 | S41 | `&kp O` | R3 C4 |
| 24 | S40 | `&kp P` | R3 C3 |
| 25 | S39 | `&kp LBKT` | R3 C2 |
| 26 | S38 | `&kp RBKT` | R3 C1 |
| 27 | S37 | `&kp BSLH` | R3 C0 |
| 28 | S36 | `&kp CAPS` | R2 C13 |
| 29 | S35 | `&kp A` | R2 C12 |
| 30 | S34 | `&kp S` | R2 C11 |
| 31 | S33 | `&kp D` | R2 C10 |
| 32 | S32 | `&kp F` | R2 C9 |
| 33 | S31 | `&kp G` | R2 C8 |
| 34 | S30 | `&kp H` | R2 C7 |
| 35 | S29 | `&kp J` | R2 C6 |
| 36 | S28 | `&kp K` | R2 C5 |
| 37 | S27 | `&kp L` | R2 C4 |
| 38 | S26 | `&kp SEMI` | R2 C3 |
| 39 | S25 | `&kp APOS` | R2 C2 |
| 40 | S24 | `&kp RET` | R2 C0 |
| 41 | S23 | `&kp LSHFT` | R1 C13 |
| 42 | S22 | `&kp Z` | R1 C12 |
| 43 | S21 | `&kp X` | R1 C11 |
| 44 | S20 | `&kp C` | R1 C10 |
| 45 | S19 | `&kp V` | R1 C9 |
| 46 | S18 | `&kp B` | R1 C8 |
| 47 | S17 | `&kp N` | R1 C7 |
| 48 | S16 | `&kp M` | R1 C6 |
| 49 | S15 | `&kp COMMA` | R1 C5 |
| 50 | S14 | `&kp DOT` | R1 C4 |
| 51 | S13 | `&kp FSLH` | R1 C3 |
| 52 | S12 | `&kp GRAVE` | R1 C2 |
| 53 | S11 | `&kp UP` | R1 C1 |
| 54 | S10 | `&kp DEL` | R1 C0 |
| 55 | S09 | `&kp LCTRL` | R0 C13 |
| 56 | S08 | `&kp LGUI` | R0 C12 |
| 57 | S07 | `&kp LALT` | R0 C11 |
| 58 | S06 | `&kp SPACE` | R0 C8 |
| 59 | S05 | `&kp RALT` | R0 C4 |
| 60 | S04 | `&mo 1` | R0 C3 |
| 61 | S03 | `&kp LEFT` | R0 C2 |
| 62 | S02 | `&kp DOWN` | R0 C1 |
| 63 | S01 | `&kp RIGHT` | R0 C0 |

Unused matrix nodes: R0 C5, C6, C7, C9, C10; R2 C1. They have no keymap bindings.

## Battery and switch

```text
Battery +  ── switch ── B+ on controller
Battery −  ─────────── B− on controller
```

This is the wiring confirmed by the owner: the switch interrupts only the positive battery lead. It is a physical battery disconnect, not a GPIO or firmware soft-off button. With USB connected, the board may remain powered while the battery switch is off; the disconnected battery cannot charge through that open lead.

Before soldering a replica, verify the exact SuperMini revision's B+/B− pad labels, polarity, battery chemistry and charger suitability. Insulate the battery and all exposed joints. The `nice_nano_v2` build target does not certify the charger or battery-measurement circuit of every SuperMini clone. Battery state-of-charge accuracy has not been validated here.

The modified case opening and controller support will be documented when the owner's photos and 3MF files are supplied.
