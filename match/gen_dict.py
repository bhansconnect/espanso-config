#!/usr/bin/env python3

import csv
import sys

from glob import glob
from os import path
from pathlib import Path


args = sys.argv
if len(args) != 2:
    print(f'Expected to be called with only a dictionary name, but got: {args}')
    exit(1)

input_name = args[1]
script_path = Path(path.realpath(__file__))
input_path = script_path.with_name(input_name)
if not path.exists(input_path):
    print(f'Could not find dictionary: {input_path}')
    exit(1)

# Load all other dictionaries to ensure no collisions.
triggers = {}
for dict_path in script_path.parent.glob('*.csv'):
    if path.normpath(dict_path) == path.normpath(input_path):
        continue

    with open(dict_path) as dict_file:
        dict_csv = csv.reader(dict_file, delimiter=',')
        for row in dict_csv:
            # For these, just skip anything malformed
            if len(row) != 2:
                continue
            triggers[row[0]] = row[1]

out = '''\
#######  DO NOT EDIT   #######
####### AUTO GENERATED #######

matches:\
'''
with open(input_path) as in_file:
    in_csv = csv.reader(in_file, delimiter=',')
    for row in in_csv:
        if len(row) != 2:
            print(f'Malformed row: {row}')
            exit(1)
        if row[0] in triggers:
            print(f'Trigger not unique: {row[0]} -> [{triggers[row[0]]}, {row[1]}]')
            exit(1)
        triggers[row[0]] = row[1]
        out += f'\n  - trigger: "{row[0]}"\n    replace: "{row[1]}"\n    propagate_case: true\n    word: true'

output_path = input_path.with_suffix('.yml')
with open(output_path, 'w') as out_file:
    out_file.write(out + '\n')
