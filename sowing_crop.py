import argparse
import pandas as pd
from datetime import datetime, timedelta
import ast

def arg_as_list(s):                                                            
    v = ast.literal_eval(s)                                                    
    if type(v) is not list:                                                    
        raise argparse.ArgumentTypeError("Argument \"%s\" is not a list" % (s))
    return v    

class Crop:
    def __init__(self, df, sowing_date, breed='rice', breakpoints = [200, 650, 950, 1100, 1250, 1700]):
        self.df = df
        self.sowing_date = datetime.strptime(sowing_date, '%Y-%m-%d').date()
        self.breed = breed
        self.breakpoints = breakpoints

    def thermal2code(self, accu_thermal):
        for i in range(len(self.breakpoints)-1,-1,-1):
            if accu_thermal > self.breakpoints[i]:
                if i+2 > len(self.breakpoints):
                    return None
                return f'v{i+2}'
        return 'v1'

    def generate_df(self):
        crop_df = {'date':[], 'period':[], 'avg_temp':[], 'min_temp':[], 'max_temp':[], 'temp_diff':[], 'rain':[]}
        daily_thermal = 0
        cur_date = self.sowing_date
        for i in range(len(self.df)):
            date = datetime.strptime(self.df['date'][i], '%Y-%m-%d').date()
            # print(date, cur_date)
            if date == cur_date:
                daily_thermal += (min(40, self.df['temp_max_date'][i]) + min(40, self.df['temp_min_date'][i])) / 2 - 10
                period = self.thermal2code(daily_thermal)
                if period == None:
                    break
                crop_df['date'].append(cur_date)
                crop_df['period'].append(self.thermal2code(daily_thermal))
                crop_df['avg_temp'].append(self.df['temp_date'][i])
                crop_df['min_temp'].append(self.df['temp_min_date'][i])
                crop_df['max_temp'].append(self.df['temp_max_date'][i])
                crop_df['temp_diff'].append(round(self.df['temp_max_date'][i]-self.df['temp_min_date'][i],2))
                crop_df['rain'].append(self.df['rain_date'][i])
                cur_date = cur_date + timedelta(days=1)
        
        return crop_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input File Path', default='preprocessed.csv')
    parser.add_argument('-s', '--sowing_date', help='Sowing Date, e.g. 1979-01-01')
    parser.add_argument('-b', '--breed', help='Breed, e.g. Rice', default='rice')
    parser.add_argument('-t', '--thermal', type=arg_as_list, default=[200, 650, 950, 1100, 1250, 1700], help="list of thermal breaking points e.g. '[200, 650, 950, 1100, 1250, 1700]'")
    parser.add_argument('-o', '--output', help='Output File Path', default='cropped.csv')

    args = parser.parse_args()

    if args.input:
        print(f'Cropping {args.input}...')
        df = pd.read_csv(args.input)

        crop = Crop(df, args.sowing_date, args.breed, args.thermal)
        crop_df = crop.generate_df()

        pd.DataFrame(crop_df).to_csv(args.output, index=False)
        print(f'Cropped file saved at {args.output}')