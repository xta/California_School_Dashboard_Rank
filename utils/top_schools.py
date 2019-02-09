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
Input Columns (Academic Indicator)
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

Public Schools
    0   CDSCode
    3   StatusType
    7   Street
    9   City
    10  Zip
    11  State
    17  Phone
    19  WebSite
    27  SOC
    28  SOCType
    30  EdOpsName
    31  EILCode
    32  EILName
    36  Magnet
    37  Latitude
    38  Longitude
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
    'ReportingYear',
    'StatusType',
    'Street',
    'City',
    'Zip',
    'State',
    'Phone',
    'WebSite',
    'SOC',
    'SOCType',
    'EdOpsName',
    'EILCode',
    'EILName',
    'Magnet',
    'Latitude',
    'Longitude'
    ]

math_file   = sys.argv[1]
engl_file   = sys.argv[2]
school_file = sys.argv[3]

schools = {}

## math

with open(math_file) as math:
    csv_reader = csv.reader(math)
    next(csv_reader)

    for math_row in csv_reader:
        school_id       = math_row[0]
        status_level    = math_row[8]
        math_status     = math_row[7]

        # TODO: refactor `school_data` to use object instead of list
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
                math_row[9],        # 'ReportingYear'
                '',                 # 'StatusType', - placeholder
                '',                 # 'Street', - placeholder
                '',                 # 'City', - placeholder
                '',                 # 'Zip', - placeholder
                '',                 # 'State', - placeholder
                '',                 # 'Phone', - placeholder
                '',                 # 'WebSite', - placeholder
                '',                 # 'SOC', - placeholder
                '',                 # 'SOCType', - placeholder
                '',                 # 'EdOpsName', - placeholder
                '',                 # 'EILCode', - placeholder
                '',                 # 'EILName', - placeholder
                '',                 # 'Magnet', - placeholder
                '',                 # 'Latitude', - placeholder
                ''                  # 'Longitude' - placeholder
            ]
            schools[school_id] = school_data

## english

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

## school info


with open(school_file) as school:
    csv_reader = csv.reader(school)
    next(csv_reader)

    for school_row in csv_reader:
        school_id = school_row[0]

        if school_id in schools:

            # note: mixing underscore and Caps is not ideal
            schools[school_id][10] = school_row[3]    # school_StatusType
            schools[school_id][11] = school_row[7]    # school_Street
            schools[school_id][12] = school_row[9]    # school_City
            schools[school_id][13] = school_row[10]   # school_Zip
            schools[school_id][14] = school_row[11]   # school_State
            schools[school_id][15] = school_row[17]   # school_Phone
            schools[school_id][16] = school_row[19]   # school_WebSite
            schools[school_id][17] = school_row[27]   # school_SOC
            schools[school_id][18] = school_row[28]   # school_SOCType
            schools[school_id][19] = school_row[30]   # school_EdOpsName
            schools[school_id][20] = school_row[31]   # school_EILCode
            schools[school_id][21] = school_row[32]   # school_EILName
            schools[school_id][22] = school_row[36]   # school_Magnet
            schools[school_id][23] = school_row[37]   # school_Latitude
            schools[school_id][24] = school_row[38]   # school_Longitude

## filter (only 5s)

top_schools = {k: v for k, v in schools.items() if v[8] == '5'}

## filter (only active)

active_schools = {k: v for k, v in top_schools.items() if v[10] == 'Active'}

## sort in descending order by combined_status

sorted_schools = sorted(active_schools.items(), key=lambda x: x[1][7], reverse=True)

## output

csv_writer = csv.writer(sys.stdout)

csv_writer.writerow(header_out)

for school in sorted_schools:
    data = school[1]
    csv_writer.writerow(data)
