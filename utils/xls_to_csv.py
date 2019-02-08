# -*- coding: utf-8 -*-

import xlrd
import csv
import sys

'''
Purpose
    convert xls/xlsx file to CSV file

Setup
    pip3 install xlrd

Usage
    python3 xls_to_csv.py file.xls > file.csv

'''

input_file  = sys.argv[1]
workbook    = xlrd.open_workbook(input_file)

# Uses 1st sheet only
worksheet   = workbook.sheet_by_index(0)

csv_writer  = csv.writer(sys.stdout)

for row_num in range(worksheet.nrows):
    row = worksheet.row_values(row_num)
    csv_writer.writerow(row)
