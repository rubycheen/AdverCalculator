import json
import argparse
import pandas as pd
from json_logic import jsonLogic

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', help='Data File Path', default='cropped.csv')
    parser.add_argument('-c', '--cond', help='Condition File Path', default='conditions.json')
    parser.add_argument('-o', '--output', help='Output File Path', default='result.json')

    args = parser.parse_args()

    if args.data and args.cond:
        print(f'Calculating {args.data}...')
        df = pd.read_csv(args.data)
        with open(args.cond, 'r') as f:
            conditions = json.load(f)  

        cond_cnts = {}
        for c in conditions:
            cnt = 0
            for idx, row in df.iterrows():
                if jsonLogic(conditions[c], row.to_dict()):
                    cnt+=1
            cond_cnts[c] = cnt

        with open(args.output, 'w') as fp:
            json.dump(cond_cnts, fp)

        print(f'Result saved at {args.output}')