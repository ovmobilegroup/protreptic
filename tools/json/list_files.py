#!/usr/bin/env python3
"""List new character source files and check if they exist."""
import os, json

SOURCE_DIR = '/opt/data/workspace/Protreptic/tools/json'
NEW_FILES = [
    'ES-FER-001.json', 'ES-CHA-001.json', 'ES-FRA-001.json','ES-ASU-001.json',
    'PT-HEN-001.json', 'PT-VAS-001.json', 'PT-SAL-001.json','PT-SPI-001.json',
    'ES-PID-001.json', 'GR-JUS-001.json', 'GR-PER-001.json','GR-VEN-001.json', 'RU-PRK-001.json'
]
for f in NEW_FILES:
    path = os.path.join(SOURCE_DIR, f)
    exists = 'EXISTS' if os.path.exists(path) else 'MISSING'
    print(f'{exists}: {f}')

