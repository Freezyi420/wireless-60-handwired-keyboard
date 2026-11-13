#!/usr/bin/env python3
"""Validate scan geometry, public assignments and retained Fn controls."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIELD = ROOT / 'boards/shields/handwired60'


def require(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


def bindings(layer):
    source = (ROOT / 'config/handwired60.keymap').read_text()
    match = re.search(r'\b' + layer + r'\s*\{\s*bindings\s*=\s*<(.*?)>;', source, re.S)
    require(match is not None, 'Missing layer ' + layer)
    return [' '.join(x.split()) for x in re.findall(r'&[^&]+', match[1])]


def main():
    overlay = (SHIELD / 'handwired60.overlay').read_text()
    coords = [tuple(map(int, x)) for x in re.findall(r'RC\((\d+),\s*(\d+)\)', overlay)]
    expected = ([(4, c) for c in range(13, -1, -1)]
                + [(3, c) for c in range(13, -1, -1)]
                + [(2, c) for c in list(range(13, 1, -1)) + [0]]
                + [(1, c) for c in range(13, -1, -1)]
                + [(0, c) for c in [13, 12, 11, 8, 4, 3, 2, 1, 0]])
    require(coords == expected, 'Transform differs from the working wiring')
    require(len(coords) == len(set(coords)) == 64, 'Expected 64 unique scan positions')
    require('columns = <14>' in overlay and 'rows = <5>' in overlay, 'Matrix dimensions')
    require('diode-direction = "col2row"' in overlay, 'Diode direction')
    require('nfct-pins-as-gpios' in overlay, 'NFC pins must be usable as GPIOs')
    pins = re.findall(r'<&gpio(\d)\s+(\d+)\s', overlay)
    expected_pins = [(0,6),(0,8),(0,17),(0,20),(0,22),(0,24),(1,0),
                     (0,11),(1,4),(1,6),(0,31),(0,29),(0,2),(1,15),
                     (1,13),(1,11),(0,10),(0,9),(1,7)]
    require([tuple(map(int,p)) for p in pins] == expected_pins, 'GPIO wiring changed')
    require(len(set(pins)) == 19, 'GPIOs must be unique')

    base = bindings('default_layer')
    fn = bindings('fn_layer')
    require(len(base) == len(fn) == 64, 'Each layer must have 64 bindings')
    reference = '''ESC N1 N2 N3 N4 N5 N6 N7 N8 N9 N0 MINUS EQUAL BSPC
TAB Q W E R T Y U I O P LBKT RBKT BSLH
CAPS A S D F G H J K L SEMI APOS RET
LSHFT Z X C V B N M COMMA DOT FSLH GRAVE UP DEL
LCTRL LGUI LALT SPACE RALT FN LEFT DOWN RIGHT'''.split()
    require(base == ['&mo 1' if k == 'FN' else '&kp '+k for k in reference],
            'Base keymap differs from the designer-linked ANSI reference')
    expected_fn = ['&trans'] * 64
    for i in range(1, 13):
        expected_fn[i] = '&kp F' + str(i)
    expected_fn[13] = '&bt BT_CLR'
    for i in range(5):
        expected_fn[15+i] = '&bt BT_SEL ' + str(i)
    expected_fn[40] = '&out OUT_BLE'
    expected_fn[58] = '&out OUT_USB'
    require(fn == expected_fn, 'Fn layer differs from the working personal firmware')

    fallback = (SHIELD / 'handwired60.keymap').read_text()
    require('#include "../../../config/handwired60.keymap"' in fallback,
            'Shield fallback must include canonical keymap')
    editor = json.loads((ROOT / 'config/handwired60.json').read_text())['layouts']['default_transform']['layout']
    require([(k['row'],k['col']) for k in editor] == coords, 'Editor scan coordinates disagree')
    physical = re.findall(r'<&key_physical_attrs\s+([^>]+)>', (SHIELD / 'handwired60-layouts.dtsi').read_text())
    expected_physical = [[round(k.get('u',1)*100),100,round(k['x']*100),round(k['y']*100),0,0,0] for k in editor]
    require([list(map(int,k.split())) for k in physical] == expected_physical,
            'Physical layout must describe all 64 editor positions in the same order')
    for p in ROOT.rglob('*'):
        if p.suffix in {'.conf','.keymap','.overlay','.dtsi'}:
            content = p.read_text()
            require(not re.search(r'CONFIG_ZMK_BLE_(EXPERIMENTAL_SEC|PASSKEY_ENTRY)', content),
                    'Unexpected personal Bluetooth setting in '+str(p))
            require('omarchy' not in content.lower(), 'Personal OS setting in '+str(p))
    metadata = (SHIELD / 'handwired60.zmk.yml').read_text()
    require('studio' not in metadata and 'example.com' not in metadata, 'Template metadata remains')
    print('PASS: 64 keys/layer, unchanged 5x14 wiring, 19 GPIOs, ANSI base, Fn controls and physical/editor geometry')


if __name__ == '__main__':
    main()
