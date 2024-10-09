import pandas as pd
import os.path

def main(output_file1, output_file2):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'nyc_311_limit.2020.csv'), header=None)

    start_index = 1
    end_index = 2
    zip_index = 8

    df.dropna(subset=[end_index, zip_index], inplace=True)
    df[start_index] = pd.to_datetime(df[start_index])
    df[end_index] = pd.to_datetime(df[end_index])
    df = df[df[start_index] <= df[end_index]]
    
    df['hour difference'] = (df[end_index]-df[start_index]) / pd.Timedelta(hours=1)
    df['month'] = df[start_index].dt.month
    df['zipcode'] = pd.to_numeric(df[zip_index], downcast='integer')

    df = df[['month', 'zipcode', 'hour difference']]
    zipcode_df = df.groupby(['zipcode', 'month'], as_index=False).mean()
    total_df = df[['month', 'hour difference']].groupby(['month'], as_index=False).mean()

    zipcode_df.to_csv(os.path.join(os.path.dirname(__file__), output_file1), index=False)
    total_df.to_csv(os.path.join(os.path.dirname(__file__), output_file2), index=False)


if __name__ == '__main__':
    main('nyc_311_limit.2020.preprocessedbyzip.csv', 'nyc_311_limit.2020.preprocessedtotal.csv')