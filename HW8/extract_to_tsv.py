import argparse
import json
import os.path
import random

cur_dir = os.path.dirname(__file__)

def main(output_file, json_file, num_posts_to_output):
    with open(os.path.join(cur_dir, json_file), 'r', encoding='utf-8') as f:
        file = json.load(f)
        posts = file['data']['children']
        if num_posts_to_output < len(posts):
            posts = random.sample(posts, k=num_posts_to_output)

        header = 'Name\ttitle\tcoding\n'
        with open(os.path.join(cur_dir, output_file), 'w+') as out:
            out.write(header)
            for p in posts:
                out.write(p['data']['author_fullname']+'\t')
                out.write(p['data']['title']+'\t')
                out.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('file', help='Json file to parse')
    parser.add_argument('num', type=int, help='Number of posts to output to file')
    args = parser.parse_args()
    main(args.output, args.file, args.num)