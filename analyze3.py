import sqlite_save as sql
pd = sql.pd
import numpy as np
import datetime

CDS_THRESHOLD = 100


def get_dark_time(df):
    is_dark = np.array(df['value'] > CDS_THRESHOLD)
    div = is_dark[1:] * 1 - is_dark[:-1] * 1
    
    up = np.where(div == 1)[0]  # become dark
    down = np.where(div == -1)[0]  # become bright
    
    df_up = df.iloc[up].copy()
    df_up["event"] = "up"

    df_down = df.iloc[down].copy()
    df_down['event'] = 'down'
    
    df_time = pd.concat([df_up, df_down], axis=0).sort_index()
    
    def get_event_type(up, down):
        if dark_hour < 1:
            event = '外出'
        elif 10 <= up.hour <= 15:
            event = '外出'
        elif 10 <= down.hour <= 18:
            event = '外出'
        else:
            event = '睡眠'
        return event


    l = list()
    for i in range(df_time.shape[0]-1):
        if (df_time['event'].iloc[i] == 'up') and (df_time['event'].iloc[i+1] == 'down'):
            up = df_time['datetime'].iloc[i]
            down = df_time['datetime'].iloc[i+1]
            dark = down - up
            dark_hour = dark / datetime.timedelta(hours=1)
            event = get_event_type(up, down)

            s = pd.Series({
                    'up': up.strftime('%H:%M'),
                    'down': down.strftime('%H:%M'),
                    'dark': round(dark_hour, 1),
                    'type': event,
                }, name=(down - datetime.timedelta(hours=8)).strftime('%Y/%m/%d'))
            l.append(s)

    if (df_time['event'].iloc[-1] == 'up'):
        up = df_time['datetime'].iloc[-1]
        down = datetime.datetime.now()
        dark = down - up
        dark_hour = dark / datetime.timedelta(hours=1)
        event = get_event_type(up, down)

        s = pd.Series({
            'up': up.strftime('%H:%M'),
            'down': "NOW: " + down.strftime('%H:%M'),
            'dark': round(dark_hour, 1),
            'type': 'NOW',
        }, name=(down-datetime.timedelta(hours=8)).strftime('%Y/%m/%d'))
        l.append(s)

    df_event = pd.concat(l, axis=1).T
   
    df_sleep = df_event
    df_sleep.to_csv('./sleep3.csv')
    df_sleep.to_csv('/var/www/html/sleep3.csv')
    return df_sleep


if __name__ == "__main__":
    df = sql.load()
    print(get_dark_time(df))


