from argparse import ArgumentParser
import os.path
import pandas as pd
from datetime import datetime

def main(**kwargs):
    print('kwargs', kwargs['output'])
    start_date = pd.to_datetime(kwargs['startdate'])
    end_date = pd.to_datetime(kwargs['enddate'])

    file = os.path.join(os.path.dirname(__file__), kwargs['input'])
    df = pd.read_csv(file, header=None)

    unique_index = 0
    open_date_index = 1
    complaint_index = 5
    borough_index = 25

    df[open_date_index] = pd.to_datetime(df[open_date_index])
    df = df[(start_date <= df[1]) & (df[1] <= end_date)]
    df = df[[unique_index, complaint_index, borough_index]]

    grouped = df.groupby([complaint_index, borough_index], as_index=False).count()
    grouped.columns = ['complaint type', 'borough', 'count']
    print(kwargs['output'])
    if kwargs['output']:
        print(kwargs['output'])
        grouped.to_csv(os.path.join(os.path.dirname(__file__), kwargs['output']), index=False)
    else:
        print(grouped.to_string(index=False))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='input file')
    parser.add_argument('-s', '--startdate', required=True, type=lambda d: datetime.strptime(d, '%m/%d/%Y').date(), help="Start date in the format yyyymmdd")
    parser.add_argument('-e', '--enddate', required=True, type=lambda d: datetime.strptime(d, '%m/%d/%Y').date(), help="End date in the format yyyymmdd")
    parser.add_argument('-o', '--output', help='output file name')

    args = parser.parse_args()
    main(**vars(args))