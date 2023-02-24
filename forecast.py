import argparse
import pandas as pd
import ast
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange

def arg_as_list(s):                                                            
    v = ast.literal_eval(s)                                                    
    if type(v) is not list:                                                    
        raise argparse.ArgumentTypeError("Argument \"%s\" is not a list" % (s))
    return v

def allDays(y, m):
    return ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]


def date2str(date):

    ld_str = f'{date.year}-'
    if date.month // 10 == 0:
        ld_str += f'0{date.month}-'
    else:
        ld_str += f'{date.month}-'
    if date.day // 10 == 0:
        ld_str += f'0{date.day}'
    else:
        ld_str += f'{date.day}'
    
    return ld_str


def predict(data, temp_pred):
    
    df = pd.read_csv(data)
    # print(df.head())
    last_month = datetime.strptime(df['date'][len(df)-1][:-3], '%Y-%m').date()
    # print(f'last_month: {last_month}')


    # print(datetime.strptime(df['date'][len(df)-1], '%Y-%m-%d').year, datetime.strptime(df['date'][0], '%Y-%m-%d').year)
    total_year = datetime.strptime(df['date'][len(df)-1], '%Y-%m-%d').year-datetime.strptime(df['date'][0], '%Y-%m-%d').year+1
    # print(f'total_year {total_year}')
    
    df_date = df.set_index('date', drop=True)

    prediction = {'date': [], 'temp': []}
    for i in range(len(temp_pred)):
        next_date = last_month + relativedelta(months=i+1)
        predict_date = allDays(next_date.year, next_date.month)
        for d in predict_date:
            avg_temp = []
            for y in range(total_year):
                ld = datetime.strptime(d, '%Y-%m-%d') - relativedelta(years=y+1)
                ld_str = date2str(ld)
                avg_temp.append(df_date['temp_date'][ld_str])
            # print(d, round(sum(avg_temp)/len(avg_temp)+temp_pred[i], 2))
            prediction['date'].append(d)
            prediction['temp'].append(round(sum(avg_temp)/len(avg_temp)+temp_pred[i], 2))

    return prediction

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input File Path', default='preprocessed.csv')
    parser.add_argument('-t', '--temp_pred', type=arg_as_list, default=[0.5, 0, -0.5], help="list of thermal breaking points e.g. '[0.5, 0, -0.5]'")
    parser.add_argument('-o', '--output', help='Output File Path', default='forecast.csv')

    args = parser.parse_args()

    if args.input:
        print(f'Predicting {args.input}...')
        output = predict(args.input, args.temp_pred)
        output_df = pd.DataFrame(output)
        output_df.to_csv((args.output), index=False)
        print(f'File saved at {args.output}')
