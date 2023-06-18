#!/usr/bin/env python3

import csv
import sys

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

out = '''
#######  DO NOT EDIT   #######
####### AUTO GENERATED #######

matches:\
'''

with open(input_path) as in_file:
    in_csv = csv.reader(in_file, delimiter=',')
    for row in in_csv:
        out += f'\n  - trigger: "{row[0]}"\n    replace: "{row[1]}"\n    propagate_case: true\n    word: true'

output_path = input_path.with_suffix('.yml')
with open(output_path, 'w') as out_file:
    out_file.write(out + '\n')
