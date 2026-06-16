# -*- coding: utf-8 -*-
"""Translate move names in packs/moves.db to French."""
import json
import shutil
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from moves_fr import MOVES_FR

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'packs', 'moves.db')
BAK_PATH = DB_PATH + '.bak'

# Pokérole-specific moves and aliases with no official French name
MANUAL_FR = {
    # Alias: different spelling in PokeAPI vs game
    'Vice Grip': 'Force Poigne',
    # Pokérole custom moves — translated manually
    'Stabilize An Ally': 'Stabiliser un Allié',
    'Cover An Ally': 'Couvrir un Allié',
    'Help Another': 'Aider un Allié',
    'Grapple': 'Grappin',
    'Run Away': 'Fuite',
    'Struggle Throw': 'Lutte Lancer',
    'Struggle (Physical)': 'Lutte (Physique)',
    'Struggle (Special)': 'Lutte (Spéciale)',
    'Ambush': 'Embuscade',
    'Clash': 'Choc',
    'Curse (Non-Ghost)': 'Malédiction (Non-Spectre)',
    'Evasion': 'Esquive',
}


def normalize(s):
    """Normalize a move name for fuzzy matching."""
    s = s.strip()
    s = s.replace('’', "'").replace('‘', "'")  # curly apostrophes
    s = s.lower()
    s = s.replace('-', ' ')
    return s


# Build normalized lookup for MOVES_FR
norm_lookup: dict[str, str] = {}
for en, fr in MOVES_FR.items():
    norm_lookup[normalize(en)] = fr


def translate(name: str) -> str | None:
    """Return French name for an English move name, or None if not found."""
    if name in MOVES_FR:
        return MOVES_FR[name]
    if name in MANUAL_FR:
        return MANUAL_FR[name]
    n = normalize(name)
    if n in norm_lookup:
        return norm_lookup[n]
    return None


def main():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]

    shutil.copy2(DB_PATH, BAK_PATH)
    print(f'Backup: {BAK_PATH}')

    translated = 0
    skipped = []
    out_lines = []

    for line in lines:
        data = json.loads(line)
        name = data.get('name', '')
        fr = translate(name)
        if fr:
            data['name'] = fr
            translated += 1
        else:
            skipped.append(name)
        out_lines.append(json.dumps(data, ensure_ascii=False, separators=(',', ':')))

    with open(DB_PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f'Translated: {translated}/{len(lines)}')
    if skipped:
        print(f'Skipped ({len(skipped)}): {skipped}')
    else:
        print('All moves translated!')


if __name__ == '__main__':
    main()
