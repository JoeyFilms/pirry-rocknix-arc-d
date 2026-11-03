#!/usr/bin/env python3
"""Build the installer-only archive; never include settings or emulator binaries.

SPDX-License-Identifier: GPL-2.0-or-later
"""
import argparse
import hashlib
from pathlib import Path
import zipfile


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'downloads/Pirry-Complete-1.6.2-ARC-D.zip')
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    files = [
        (root / 'Install-Saturn-Pirry.sh', 'Install-Saturn-Pirry.sh'),
        (root / 'Disable-Pirry-in-Saturn.sh', 'Disable-Pirry-in-Saturn.sh'),
        (root / 'INSTALL.txt', 'README.txt'),
    ]
    for source in sorted((root / 'pirry-arc').rglob('*')):
        if source.is_file() and '__pycache__' not in source.parts:
            if source.suffix not in {'.sh', '.py', '.json', '.txt'}:
                raise RuntimeError('Unexpected payload file: ' + str(source))
            files.append((source, source.relative_to(root).as_posix()))
    for source, _ in files:
        if not source.is_file() or not source.stat().st_size:
            raise RuntimeError('Missing or empty package source: ' + str(source))
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for source, name in files:
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 3, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if source.suffix == '.sh' else 0o100644) << 16
            archive.writestr(info, source.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('ZIP integrity check failed')
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    (output.parent / 'SHA256SUMS').write_text(digest + '  ' + output.name + '\n')
    print(str(output))
    print(digest)


if __name__ == '__main__':
    main()
