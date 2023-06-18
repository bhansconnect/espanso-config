#!/usr/bin/env python3
import csv

from os import path
from pathlib import Path

out = '''
#######  DO NOT EDIT   #######
####### AUTO GENERATED #######

matches:\
'''

script_path = Path(path.realpath(__file__))
input_path = script_path.with_name('dict.csv')
with open(input_path) as in_file:
    in_without_comments = filter(lambda row: row.strip() and not row.startswith('#'), in_file)
    in_csv = csv.reader(in_without_comments)
    triggers = set()
    for row in in_csv:
        if len(row) != 2:
            print(f'Malformed row: {row}')
            exit(1)
        if row[0] in triggers:
            print(f'Trigger not unique: {row[0]}')
            exit(1)
        triggers.add(row[0])
        out += f'\n  - trigger: "{row[0]}"\n    replace: "{row[1]}"\n    propagate_case: true\n    word: true'

output_path = input_path.with_suffix('.yml')
with open(output_path, 'w') as out_file:
    out_file.write(out + '\n')
