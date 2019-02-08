# California School Dashboard Rank

Analysis of [CA School Dashboard](https://www.caschooldashboard.org/) [data](https://www.cde.ca.gov/ta/ac/cm/)

## Build data

    python3 utils/xls_to_csv.py resources/mathdownload2018.xlsx | python3 utils/filter_csv.py > data/math_2018_academic_indicator.csv
    python3 utils/xls_to_csv.py resources/eladownload2018.xlsx | python3 utils/filter_csv.py > data/english_2018_academic_indicator.csv

    python3 utils/top_schools.py data/math_2018_academic_indicator.csv data/english_2018_academic_indicator.csv > data/top_schools_2018_by_math_and_english.csv
