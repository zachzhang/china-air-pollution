import pandas as pd
import os
import datetime
from tstoolbox.tstoolbox import fill


def parse_date(x):
    date_string = str(x['date'])

    year = int(date_string[:4])
    month = int(date_string[4:6])
    day = int(date_string[6:])
    hour = int(x['hour'])

    return datetime.datetime(year, month, day, hour)

def iter_dir(dir):

    files = os.listdir(dir)
    df = []

    for file in files:

        if file == '.DS_Store':
            continue

        df.append(pd.read_csv( dir + '/' + file))

    return pd.concat(df)


def load_aqi():

    #load raw data
    df15 = iter_dir('./2015')
    df16 = iter_dir('./2016')
    df = pd.concat([df15,df16])

    #just select AQI for now
    aqi = df[df['type'] == 'AQI']

    #parse into datetime
    aqi['datetime'] = aqi.apply(lambda x: parse_date(x), axis=1)

    #fill in missing entries with NaN
    aqi = aqi.set_index('datetime').resample('H').asfreq()

    #linearly interpolate missing entries
    imputed_data = fill(method='linear', input_ts=aqi)

    return imputed_data