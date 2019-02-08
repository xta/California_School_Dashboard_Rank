# -*- coding: utf-8 -*-

import csv
import sys

'''
Purpose
    Filter a CSV in known schema (Academic Indicator) by arbitrary criteria

Usage
    python3 top_schools.py math_file.csv english_file.csv > file_out.csv

'''

'''
Input Columns
    0 - cds
    1 - rtype
    2 - schoolname
    3 - districtname
    4 - countyname
    5 - charter_flag
    6 - studentgroup
    7 - currstatus
    8 - statuslevel
    9 - ReportingYear
'''

header_out = [
    'cds',
    'schoolname',
    'districtname',
    'countyname',
    'charter_flag',
    'math_status',
    'english_status',
    'combined_status',
    'status_level', # only use math for now
    'ReportingYear'
    ]

math_file = sys.argv[1]
engl_file = sys.argv[2]

schools = {}

## math

with open(math_file) as math:
    csv_reader = csv.reader(math)
    next(csv_reader)

    for math_row in csv_reader:
        school_id       = math_row[0]
        status_level    = math_row[8]
        math_status     = math_row[7]

        if status_level != 0 and math_status is not '':
            school_data = [
                math_row[0],        # 'cds',
                math_row[2],        # 'schoolname',
                math_row[3],        # 'districtname',
                math_row[4],        # 'countyname',
                math_row[5],        # 'charter_flag',
                float(math_status), # 'math_status',
                0,                  # 'english_status', - placeholder
                0,                  # 'combined_status', - placeholder
                status_level,       # 'status_level',
                math_row[9]         # 'ReportingYear'
            ]
            schools[school_id] = school_data

# ## english

with open(engl_file) as english:
    csv_reader = csv.reader(english)
    next(csv_reader)

    for english_row in csv_reader:
        school_id       = english_row[0]
        status_level    = english_row[8]
        english_status  = english_row[7]

        if status_level != 0 and english_status is not '':
            if school_id in schools:
                english_status          = float(english_row[7])
                math_status             = float(schools[school_id][5])
                combined_status         = math_status + english_status
                rounded_combined        = float("%.2f" % combined_status)

                schools[school_id][6]   = english_status
                schools[school_id][7]   = rounded_combined

## filter (only 5s)

top_schools = {k: v for k, v in schools.items() if v[8] == '5'}

## sort in descending order by combined_status

sorted_schools = sorted(top_schools.items(), key=lambda x: x[1][7], reverse=True)

## output

csv_writer = csv.writer(sys.stdout)

csv_writer.writerow(header_out)

for school in sorted_schools:
    data = school[1]
    csv_writer.writerow(data)
