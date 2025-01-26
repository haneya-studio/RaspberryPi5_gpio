import sqlite_save as sql
pd = sql.pd
import numpy as np
import datetime


def get_dark_time(df):
    is_dark = np.array(df['value'] > 200)
    div = is_dark[1:] * 1 - is_dark[:-1] * 1
    up = np.where(div == 1)[0]  # become dark
    down = np.where(div == -1)[0]  # become bright

    pairs = [[up_value, down_value] for up_value, down_value in zip(list(up), list(down))]
    pairs_datetime = [list(df['datetime'].iloc[pair]) for pair in pairs]
    sleep_times = [pair[0] for pair in pairs_datetime]

    times = [(down_time - up_time) / datetime.timedelta(hours=1) for up_time, down_time in pairs_datetime]
    df_sleep = pd.DataFrame({'time': times}, index=sleep_times)
    df_sleep.to_csv('/var/www/html/sleep.csv')
    return df_sleep


if __name__ == "__main__":
    df = sql.load()
    print(get_dark_time(df))


