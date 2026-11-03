#!/usr/bin/env python3
"""Bind the ARC's raw or InputPlumber controller using its matching layout.

SPDX-License-Identifier: GPL-2.0-or-later
"""
import ctypes as C
import json
import os
from pathlib import Path
import sys
import tempfile
import time

RAW = 'rg_arc_joypad'
VIRTUAL = 'Sony Interactive Entertainment DualSense Wireless Controller'


def select_controller(devices, prefer_virtual):
    for name in ([VIRTUAL, RAW] if prefer_virtual else [RAW, VIRTUAL]):
        candidates = [device for device in devices if device[1] == name]
        if len(candidates) > 1:
            raise RuntimeError('Multiple matching controllers. Disconnect external controllers for this test.')
        if candidates:
            return candidates[0]
    raise RuntimeError('Neither ARC raw controller nor the InputPlumber DualSense controller was found.')


def bind(template, existing, identity):
    device_id, name, guid = identity
    prior_player = (existing or {}).get('player1', {})
    changed_layout = bool(existing) and prior_player.get('deviceName') != name
    source = existing if existing and not changed_layout else template
    player = source['player1']
    old_key = f"{player['DeviceID']}_{player['deviceName']}_{player['deviceGUID']}"
    if old_key not in source:
        raise ValueError('Existing controller mapping is incomplete; preserved without changing it.')
    result = dict(existing or source)
    prior_key = f"{prior_player.get('DeviceID')}_{prior_player.get('deviceName')}_{prior_player.get('deviceGUID')}"
    result.pop(prior_key, None)
    result.pop(old_key, None)
    result[f'{device_id}_{name}_{guid}'] = source[old_key]
    result['player1'] = dict(player, DeviceID=device_id, deviceName=name, deviceGUID=guid)
    return result, changed_layout


def atomic_write(path, data):
    fd, temporary = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        Path(temporary).unlink(missing_ok=True)


def update_mapping(config_dir, template, identity):
    config_dir.mkdir(parents=True, exist_ok=True)
    target = config_dir / 'keymapv2.json'
    old_bytes = target.read_bytes() if target.exists() else None
    existing = json.loads(old_bytes) if old_bytes is not None else None
    result, changed_layout = bind(template, existing, identity)
    if changed_layout:
        backup = config_dir / ('keymapv2.before-controller-change-' + str(time.time_ns()) + '.json')
        atomic_write(backup, old_bytes)
        print('Controller interface changed. Previous mapping backed up to ' + str(backup))
        print('Applying matching ROCKNIX ARC six-button layout; other game settings and saves are retained.')
    atomic_write(target, (json.dumps(result, indent=2) + '\n').encode())
    return result


def enumerate_controllers():
    sdl = C.CDLL('libSDL2-2.0.so.0')
    class GUID(C.Structure):
        _fields_ = [('data', C.c_uint8 * 16)]
    sdl.SDL_Init.argtypes = [C.c_uint32]
    sdl.SDL_JoystickOpen.argtypes = [C.c_int]
    sdl.SDL_JoystickOpen.restype = C.c_void_p
    sdl.SDL_JoystickName.argtypes = [C.c_void_p]
    sdl.SDL_JoystickName.restype = C.c_char_p
    sdl.SDL_JoystickInstanceID.argtypes = [C.c_void_p]
    sdl.SDL_JoystickGetGUID.argtypes = [C.c_void_p]
    sdl.SDL_JoystickGetGUID.restype = GUID
    sdl.SDL_JoystickGetGUIDString.argtypes = [GUID, C.c_char_p, C.c_int]
    sdl.SDL_JoystickClose.argtypes = [C.c_void_p]
    sdl.SDL_GetError.restype = C.c_char_p
    if sdl.SDL_Init(0x200) != 0:
        raise RuntimeError(sdl.SDL_GetError().decode(errors='replace'))
    devices = []
    try:
        for index in range(sdl.SDL_NumJoysticks()):
            joystick = sdl.SDL_JoystickOpen(index)
            if not joystick:
                continue
            try:
                name = sdl.SDL_JoystickName(joystick).decode()
                guid = C.create_string_buffer(33)
                sdl.SDL_JoystickGetGUIDString(sdl.SDL_JoystickGetGUID(joystick), guid, 33)
                device = (sdl.SDL_JoystickInstanceID(joystick), name, guid.value.decode())
                devices.append(device)
                print(f'SDL controller {index}: {name} ({device[2]})')
            finally:
                sdl.SDL_JoystickClose(joystick)
    finally:
        sdl.SDL_Quit()
    return devices


def main():
    config_dir = Path.home() / '.yabasanshiro'
    if not str(config_dir).startswith('/storage/'):
        raise RuntimeError('Expected ROCKNIX home under /storage; got ' + str(config_dir))
    devices = enumerate_controllers()
    identity = select_controller(devices, Path('/usr/share/inputplumber').is_dir())
    raw_template = Path(sys.argv[1])
    template_path = raw_template.with_name('arc-keymap-inputplumber.json') if identity[1] == VIRTUAL else raw_template
    template = json.loads(template_path.read_text())
    update_mapping(config_dir, template, identity)
    print(f'ARC mapping: {identity}; template: {template_path}; settings and saves: {config_dir}')


if __name__ == '__main__':
    main()
