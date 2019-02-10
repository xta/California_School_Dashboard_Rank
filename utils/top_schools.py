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

report_columns = [
    'cds',              # id
    'school_name',
    'district_name',
    'county_name',
    'charter_flag',
    'math_status',
    'english_status',
    'combined_status',
    'status_level',     # only use math for now
    'reporting_year',
    'status_type',
    'street',
    'city',
    'zip',
    'state',
    'phone',
    'web_site',
    'soc',
    'soc_type',
    'ed_ops_name',
    'eil_code',
    'eil_name',
    'magnet',
    'latitude',
    'longitude'
    ]

class School(object):
    __slots__ = report_columns

    def __init__(self, cds, school_name, district_name,
        county_name, charter_flag, math_status, status_level, reporting_year):
        self.cds            = cds
        self.school_name    = school_name
        self.district_name  = district_name
        self.county_name    = county_name
        self.charter_flag   = charter_flag
        self.math_status    = float(math_status)
        self.status_level   = status_level
        self.reporting_year = reporting_year

        self.status_type    = None
        self.street         = None
        self.city           = None
        self.zip            = None
        self.state          = None
        self.phone          = None
        self.web_site       = None
        self.soc            = None
        self.soc_type       = None
        self.ed_ops_name    = None
        self.eil_code       = None
        self.eil_name       = None
        self.magnet         = None
        self.latitude       = None
        self.longitude      = None

    def update_english_and_combined(self, english_status):
        self.english_status = float(english_status)

        combined = self.math_status + self.english_status
        self.combined_status = float("%.2f" % combined)

    def export_row(self):
        row = []
        for column in report_columns:
            row.append(getattr(self, column))
        return row

if __name__ == '__main__':

    ## state

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

            if status_level != 0 and math_status is not '':
                school_data = School(school_id,
                                math_row[2],        # school_name
                                math_row[3],        # district_name
                                math_row[4],        # county_name
                                math_row[5],        # charter_flag
                                float(math_status),
                                status_level,
                                math_row[9]         # reporting_year
                    )
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
                    schools[school_id].update_english_and_combined(english_status)

    ## school info

    with open(school_file) as school:
        csv_reader = csv.reader(school)
        next(csv_reader)

        for school_row in csv_reader:
            school_id = school_row[0]

            if school_id in schools:
                schools[school_id].status_type  = school_row[3]
                schools[school_id].street       = school_row[7]
                schools[school_id].city         = school_row[9]
                schools[school_id].zip          = school_row[10]
                schools[school_id].state        = school_row[11]
                schools[school_id].phone        = school_row[17]
                schools[school_id].web_site     = school_row[19]
                schools[school_id].soc          = school_row[27]
                schools[school_id].soc_type     = school_row[28]
                schools[school_id].ed_ops_name  = school_row[30]
                schools[school_id].eil_code     = school_row[31]
                schools[school_id].eil_name     = school_row[32]
                schools[school_id].magnet       = school_row[36]
                schools[school_id].latitude     = school_row[37]
                schools[school_id].longitude    = school_row[38]

    ## filter (only 5s)
    top_schools = {k: v for k, v in schools.items() if v.status_level == '5'}

    ## filter (only active)
    active_schools = {k: v for k, v in top_schools.items() if v.status_type == 'Active'}

    ## sort in descending order by combined_status
    sorted_schools = sorted(active_schools.items(), key=lambda x: x[1].combined_status, reverse=True)

    ## output

    csv_writer = csv.writer(sys.stdout)

    # header row
    csv_writer.writerow(report_columns)

    # data rows
    for school_tuple in sorted_schools:
        school = school_tuple[1]
        csv_writer.writerow(school.export_row())
