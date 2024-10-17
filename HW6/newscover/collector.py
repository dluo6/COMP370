'''
Write a CLI tool sitting in the newscover.collector module that has the following behavior
	python -m newscover.collector -k <api_key> [-b <# days to lookback>] -i <input_file> -o <output_dir>
The input file is a json file containing a dictionary of named keyword lists. Like this
{ “trump_fiasco”: [“trump”, “trial”], “swift”: [“taylor”, “swift”, “movie”] ]
For each keyword set with name N and keyword list X, the collector will execute a query for the keywords X and write the results to the <output_dir>/N.json.
'''
import argparse
import os.path
from .newsapi import fetch_latest_news
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', required=True, help='api key')
    parser.add_argument('-b', required=False, help='# of days to lookback')
    parser.add_argument('-i', required=True, help='input file')
    parser.add_argument('-o', required=True, help='output directory')
    args = parser.parse_args()

    cur_dir = os.path.dirname(__file__)

    if not os.path.exists(os.path.join(cur_dir, args.o)):
        os.makedirs(os.path.join(cur_dir, args.o))
    
    with open(os.path.join(cur_dir, args.i), 'r') as file:
        vars = json.load(file)

    for v in vars:
        if args.b:
            articles = fetch_latest_news(args.k, vars[v], args.b)
        else:
            articles = fetch_latest_news(args.k, vars[v])
            
        with open(os.path.join(cur_dir, args.o, v), 'w+') as file:
            file.write(str(articles))
    
if __name__ == '__main__':
    main()