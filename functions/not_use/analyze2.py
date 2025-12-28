import python.gpio.functions.sqlite_save as sql
pd = sql.pd
import numpy as np
import datetime


def get_dark_time(df):
    is_dark = np.array(df['value'] > 200)
    div = is_dark[1:] * 1 - is_dark[:-1] * 1
    
    up = np.where(div == 1)[0]  # become dark
    down = np.where(div == -1)[0]  # become bright
    
    df_up = df.iloc[up]
    df_up['event'] = 'up'
    df_down = df.iloc[down]
    df_down['event'] = 'down'
    
    df_time = pd.concat([df_up, df_down], axis=0).sort_index()
    print(df_time)
    
    l = list()
    for i in range(df_time.shape[0]-1):
        if (df_time['event'].iloc[i] == 'up') and (df_time['event'].iloc[i+1] == 'down'):
            s = pd.Series({
                    'up': df_time['datetime'].iloc[i].strftime('%H:%M'),
                    'down': df_time['datetime'].iloc[i+1].strftime('%H:%M'),
                    'sleep': round((df_time['datetime'].iloc[i+1] - df_time['datetime'].iloc[i]) / datetime.timedelta(hours=1), 1),
                }, name=(df_time['datetime'].iloc[i+1]-datetime.timedelta(days=1)).strftime('%Y/%m/%d'))
            l.append(s)
    if (df_time['event'].iloc[-1] == 'up'):
        s = pd.Series({
            'up': df_time['datetime'].iloc[i].strftime('%H:%M'),
            'down': "NOW: " + datetime.datetime.now().strftime('%H:%M'),
            'sleep': round((datetime.datetime.now().iloc[i+1] - datetime.datetime.now()) / datetime.timedelta(hours=1), 1),
        }, name=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y/%m/%d'))
    l.append(s)

    df_event = pd.concat(l, axis=1).T
    
    df_sleep = df_event
    df_sleep.to_csv('./sleep2.csv')
    df_sleep.to_csv('/var/www/html/sleep2.csv')
    return df_sleep


if __name__ == "__main__":
    df = sql.load()
    print(get_dark_time(df))


