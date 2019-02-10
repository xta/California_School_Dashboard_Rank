# California School Dashboard Rank

Analysis of [CA School Dashboard](https://www.caschooldashboard.org/) [data](https://www.cde.ca.gov/ta/ac/cm/)

## Build data (macOS)

    # Setup
    brew install coreutils
    pip3 install xlrd

    # Build data/ files
    python3 utils/xls_to_csv.py resources/mathdownload2018.xlsx | python3 utils/filter_academic_indicator_csv.py > data/math_2018_academic_indicator.csv

    python3 utils/xls_to_csv.py resources/eladownload2018.xlsx | python3 utils/filter_academic_indicator_csv.py > data/english_2018_academic_indicator.csv

    python3 utils/xls_to_csv.py resources/pubschls.xlsx | tail -n +6 | ghead -n -1 > data/public_schools.csv
    ## Note: Excel date format issue

    python3 utils/top_schools.py data/math_2018_academic_indicator.csv data/english_2018_academic_indicator.csv data/public_schools.csv > data/top_schools_2018_by_math_and_english.csv

    python3 utils/csv_to_json.py data/top_schools_2018_by_math_and_english.csv data/top_schools_2018_by_math_and_english.json schools
