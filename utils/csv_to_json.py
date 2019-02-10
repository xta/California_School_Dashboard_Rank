# -*- coding: utf-8 -*-

import sys
import csv
import json


'''
Purpose
    Convert a CSV to a JSON file

Usage
    python3 csv_to_json.py file_in.csv file_out.json json_key

'''

def row_count(file_name):
    with open(file_name) as in_file:
        return sum(1 for _ in in_file)

if __name__ == '__main__':
    assert(len(sys.argv) == 4)

    csv_file    = open(sys.argv[1], 'r')
    json_file   = open(sys.argv[2], 'w')
    json_key    = sys.argv[3]
    new_line    = '\n'

    with open(sys.argv[1]) as csv_document:

        # input

        reader = csv.reader(csv_document)
        field_names = next(reader)

        csv_reader = csv.DictReader(csv_file, field_names)
        next(csv_reader) # skip header

        # count lines (to detect last row)

        lines = row_count(sys.argv[1])
        assert(lines > 0)
        last_line = lines-2 # one for 0 based index, one for header row

        # output

        json_file.write('{ "' + json_key + '": [' + new_line)

        for index, row in enumerate(csv_reader):
            json.dump(row, json_file)

            if index != last_line:
                json_file.write(',' + new_line)
            else:
                json_file.write(new_line)

        json_file.write(']}' + new_line)
