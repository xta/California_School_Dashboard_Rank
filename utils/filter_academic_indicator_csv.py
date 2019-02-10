# -*- coding: utf-8 -*-

import csv
import sys

'''
Purpose
    Filter a CSV in known schema (Academic Indicator) by arbitrary criteria

Usage
    cat file_in.csv | python3 filter_academic_indicator_csv.py > file_out.csv

'''

'''
Columns:
    0 - cds
    1 - rtype
    2 - schoolname
    3 - districtname
    4 - countyname
    5 - charter_flag
        coe_flag
        dass_flag
    8 - studentgroup
        currdenom
        currdenom_swd
    11- currstatus
        priordenom
        priordenom_swd
        priorstatus
        change
    16- statuslevel
        changelevel
        color
        box
        hscutpoints
        curradjustment
        prioradjustment
        pairshare_method
        caa_denom
        caa_level1_num
        caa_level1_pct
        caa_level2_num
        caa_level2_pct
        caa_level3_num
        caa_level3_pct
    31- ReportingYear
'''

csv_reader = csv.reader(sys.stdin)
csv_writer = csv.writer(sys.stdout)

# filter Academic Indicator file(s)

keep_columns = [0, 1, 2, 3, 4, 5, 8, 11, 16, 31]

def get_kept_columns(row):
    header_row = []
    for index in keep_columns:
        header_row.append(row[index])
    return header_row

def keep_data_row(row):
    row_type = row[1]
    row_group = row[8]
    return row_type == 'S' and row_group == 'ALL'

for i, row in enumerate(csv_reader):
    if i == 0:
        header_row = get_kept_columns(row)
        csv_writer.writerow(header_row)
    else:
        if keep_data_row(row):
            data_row = get_kept_columns(row)
            csv_writer.writerow(data_row)
