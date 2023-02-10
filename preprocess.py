import pandas as pd
import argparse
from datetime import datetime

def preprocess(file_path, output_path):
    # read data
    df = pd.read_csv(file_path)

    df_proccessed = df[['dt','timezone','city_name',
                        'temp','temp_min','temp_max', 'rain_1h']]
    df_proccessed["rain_1h"] = df_proccessed["rain_1h"].fillna(0)

    df_proccessed['time(UTC+8)'] = df_proccessed['dt']+df_proccessed['timezone']
    df_proccessed = df_proccessed.drop(columns=['dt','timezone'])

    # get date
    df_proccessed['date'] = df_proccessed['time(UTC+8)']

    for i, d in enumerate(df_proccessed['time(UTC+8)']):
        df_proccessed['date'][i] = datetime.fromtimestamp(d).date()


    ## date merge
    date_dict = {'date': [], 'city_name_date': [],
                'temp_date': [], 'temp_min_date':[],
                'temp_max_date': [], 'rain_date': []}

    cur_date = ''
    temp_tmp, temp_min_tmp, temp_max_tmp, temp_rain = [], [], [], []

    for i, d in enumerate(df_proccessed['date']):
        if cur_date=='':
            cur_date = d
            cur_city = df_proccessed['city_name'][i]
            temp_tmp.append(df_proccessed['temp'][i])
            temp_min_tmp.append(df_proccessed['temp_min'][i])
            temp_max_tmp.append(df_proccessed['temp_max'][i])
            temp_rain.append(df_proccessed['rain_1h'][i])
        
        elif d != cur_date:
            print(cur_date)
            date_dict['date'].append(cur_date)
            date_dict['city_name_date'].append(cur_city)
            date_dict['temp_date'].append(round(sum(temp_tmp) / len(temp_tmp), 2))
            date_dict['temp_min_date'].append(min(temp_min_tmp))
            date_dict['temp_max_date'].append(max(temp_max_tmp))
            date_dict['rain_date'].append(round(sum(temp_rain), 2))

            cur_date = d
            cur_city = df_proccessed['city_name'][i]
            temp_tmp, temp_min_tmp, temp_max_tmp, temp_rain = [], [], [], []

        elif d==cur_date:
            temp_tmp.append(df_proccessed['temp'][i])
            temp_min_tmp.append(df_proccessed['temp_min'][i])
            temp_max_tmp.append(df_proccessed['temp_max'][i])
            temp_rain.append(df_proccessed['rain_1h'][i])

    # last date
    print(cur_date)
    date_dict['date'].append(cur_date)
    date_dict['city_name_date'].append(cur_city)
    date_dict['temp_date'].append(round(sum(temp_tmp) / len(temp_tmp), 2))
    date_dict['temp_min_date'].append(min(temp_min_tmp))
    date_dict['temp_max_date'].append(max(temp_max_tmp))
    date_dict['rain_date'].append(round(sum(temp_rain), 2))

    pd.DataFrame(date_dict).to_csv(output_path, index=False)
    print(f'File saved at {output_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input File Path')
    parser.add_argument('-o', '--output', help='Output File Path', default='preprocessed.csv')

    args = parser.parse_args()

    if args.input:
        print(f'Preproccessing {args.input}...')
        preprocess(args.input, args.output)