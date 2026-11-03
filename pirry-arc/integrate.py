#!/usr/bin/env python3
"""Add an emulator choice to ROCKNIX's existing Saturn system.

SPDX-License-Identifier: GPL-2.0-or-later
"""
import copy
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

MARKER = 'pirry-saturn-integration-v1'
FRAGMENT = 'es_systems_zz_pirry.cfg'
BASE = '/storage/.config/yabasanshiro-pirry'
COMMAND = ('/usr/bin/bash ' + BASE + '/runemu-pirry.sh %ROM% '
           '-Psaturn --core=pirry --emulator=pirry')
KNOWN_BINARIES = {
    '3697285df5f6586b0f32185b7384a307c0406ef815b839d6a8519b97939d5e80',
    '59d6fde43ac128bf219dec09f41bcc9a43915cd09b6af880d5d6cd119a179552',
}


def at(root, absolute):
    return root / absolute.lstrip('/')


def atomic_write(path, data, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        Path(temporary).unlink(missing_ok=True)


def make_runner(source):
    anchor = 'case ${EMULATOR} in\n'
    if source.count(anchor) != 1:
        raise RuntimeError('Unexpected runemu.sh layout; no system files changed.')
    addition = ("  pirry)\n"
                "    set_kill set \"-9 yabasanshiro-pirry\"\n"
                "    RUNTHIS='${EMUPERF} ${RUN_SHELL} " + BASE + '/run.sh "${ROMNAME}"' + "'\n"
                "  ;;\n")
    return source.replace(anchor, anchor + addition, 1)


def make_fragment(saturn):
    original = saturn.find('emulators')
    if original is None or not original.findall('emulator'):
        raise RuntimeError('No original Saturn emulator list found; stopped.')
    root = ET.Element('systemList')
    system = ET.SubElement(root, 'system')
    ET.SubElement(system, 'name').text = 'saturn'
    emulators = ET.SubElement(system, 'emulators')
    pirry = ET.SubElement(emulators, 'emulator', name='pirry', command=COMMAND)
    cores = ET.SubElement(pirry, 'cores')
    ET.SubElement(cores, 'core', default='true').text = 'pirry'
    for emulator in original.findall('emulator'):
        if emulator.get('name') == 'pirry':
            raise RuntimeError('Another pirry emulator entry already exists; stopped.')
        cloned = copy.deepcopy(emulator)
        for core in cloned.iter('core'):
            core.attrib.pop('default', None)
        emulators.append(cloned)
    ET.indent(root, space='  ')
    return (b'<?xml version="1.0" encoding="utf-8"?>\n<!-- ' + MARKER.encode() +
            b' -->\n' + ET.tostring(root, encoding='utf-8') + b'\n')


def select_base(root):
    # Matches SystemData::getConfigPath for the ROCKNIX build.
    for absolute in [
        '/storage/.config/emulationstation/es_systems_custom.cfg',
        '/storage/.config/emulationstation/es_systems.cfg',
        '/usr/bin/es_systems.cfg',
        '/etc/emulationstation/es_systems.cfg',
    ]:
        candidate = at(root, absolute)
        if candidate.is_file():
            return candidate
    raise RuntimeError('Cannot find ROCKNIX es_systems.cfg.')


def enable(root=Path('/')):
    program_dir = at(root, BASE)
    executable = program_dir / 'yabasanshiro-pirry'
    if not executable.is_file() or hashlib.sha256(executable.read_bytes()).hexdigest() not in KNOWN_BINARIES:
        raise RuntimeError('Expected verified Pirry 1.6.1 or 1.6.2 from the previous kit. Install it first.')
    if not (program_dir / 'run.sh').is_file() or not (program_dir / 'run.sh').stat().st_size:
        raise RuntimeError('Existing Pirry launcher is missing or empty.')
    user_dir = at(root, '/storage/.config/emulationstation')
    target = user_dir / FRAGMENT
    if target.exists() and MARKER not in target.read_text():
        raise RuntimeError('An unrelated file already uses the custom config filename; preserved.')
    base = select_base(root)
    saturn = ET.parse(base).getroot().find("system[name='saturn']")
    if saturn is None:
        raise RuntimeError('Saturn system missing from the main config.')
    # Other Saturn emulator/command overrides need manual reconciliation. Refuse
    # rather than relying on unspecified directory enumeration precedence.
    for directory in [user_dir, at(root, '/usr/bin')]:
        for custom in directory.glob('es_systems_*.cfg'):
            if custom == target or custom.resolve() == base.resolve():
                continue
            for system in ET.parse(custom).getroot().findall('system'):
                if system.findtext('name') == 'saturn' and (system.find('emulators') is not None or system.find('command') is not None):
                    raise RuntimeError(f'Existing custom Saturn launch configuration: {custom}. Preserved; stopped.')
    fragment = make_fragment(saturn)
    source_path = at(root, '/usr/bin/runemu.sh')
    runner = make_runner(source_path.read_text())
    # Both generated files are validated before the override becomes visible.
    ET.fromstring(fragment)
    result = subprocess.run(['bash', '-n'], input=runner, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError('Generated launcher syntax failed: ' + result.stderr)
    if target.exists():
        backup = program_dir / ('saturn-menu-backup-' + str(time.time_ns()) + '.xml')
        atomic_write(backup, target.read_bytes())
    atomic_write(program_dir / 'runemu-pirry.sh', runner.encode(), 0o755)
    atomic_write(target, fragment)
    print(f'Enabled: {target}')
    print('Restart ROCKNIX, then START > Game Settings > Per System Advanced Configuration > Saturn.')
    print('Choose emulator pirry, core pirry. Individual game overrides still take priority.')


def disable(root=Path('/')):
    target = at(root, '/storage/.config/emulationstation/' + FRAGMENT)
    if not target.exists():
        print('Already disabled.')
        return
    if MARKER not in target.read_text():
        raise RuntimeError('Custom config is not owned by this add-on; preserved.')
    disabled = target.with_name(target.name + '.disabled-' + str(time.time_ns()))
    os.replace(target, disabled)
    print('Disabled; config retained at ' + str(disabled))
    print('Restart ROCKNIX to load the original emulator list. Saves and artwork are unchanged.')


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['enable']:
            enable()
        elif sys.argv[1:] == ['disable']:
            disable()
        else:
            raise RuntimeError('Usage: integrate.py enable|disable')
    except Exception as error:
        print('FAILED: ' + str(error), file=sys.stderr)
        sys.exit(1)
