import json
import pandas as pd
from json_logic import jsonLogic
from tqdm import tqdm

from sowing_crop import Crop

df = pd.read_csv('metadata/preprocessed.csv')

with open('conditions.json', 'r') as f:
    conditions = json.load(f)  

keys = list(conditions.keys())
all_cal = {'date': []}
[all_cal.update({k: []}) for k in keys]

for i, d in enumerate(tqdm(df['date'])):
    crop = Crop(df, d)
    crop_df = pd.DataFrame(crop.generate_df())

    cond_cnts = {}
    for c in conditions:
        cnt = 0
        for idx, row in crop_df.iterrows():
            if jsonLogic(conditions[c], row.to_dict()):
                cnt+=1
        cond_cnts[c] = cnt
    all_cal['date'].append(d)
    [all_cal[k].append(cond_cnts[k]) for k in keys]

pd.DataFrame(all_cal).to_csv('history.csv', index=False)