import spidev
import time
import python.gpio.functions.sqlite_save as sql
pd = sql.pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import analyze3 as analyze

def f(num):
    binary_16bit = f'{num:08b}'  # 16ビットの2進数にゼロ埋め
    binary_8x2bit = ' '.join(binary_16bit[i:i+2] for i in range(0, len(binary_16bit), 2))
    return binary_8x2bit


class ADC0834:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 100 * 1000  # 最大通信速度（100kHz）

    def read_channel(self, channel):
        if channel < 0 or channel > 3:
            raise ValueError("Channel must be between 0 and 3.")

        # コマンド構築
        start_bit = 0x01
        mode_bit = 0x80  # シングルエンドモード
        channel_bits = channel << 4
        command = [start_bit, mode_bit | channel_bits, 0x00, 0x00]

        # SPI通信 (spidev の xfer2 メソッドを使用)
        result = self.spi.xfer2(command)

        # データ処理
        # print('{} / {} / {} / {}'.format(f(result[0]), f(result[1]), f(result[2]), f(result[3])))
        high_byte = result[1] & 0x0f  # 上位4ビット
        low_byte = result[2] & 0xf0  # 下位4ビット
        # print('{} / {}'.format(f(high_byte), f(low_byte)))
        value = (high_byte << 4) | (low_byte >> 4)
        return value

    def close(self):
        self.spi.close()


def measure(channel):
    # ADC0834 の初期化
    adc = ADC0834(bus=0, device=0)

    # チャンネル0のデータを取得
    try:
        value = adc.read_channel(channel)
        # print("Channel 0 Value: {} / {}".format(value, f(value)))
        print("Channel {} Value: {}".format(channel, value))
        sql.add(value)
        df = sql.load()
        print(df.tail(50))
        plot(df)
        analyze.get_dark_time(df)
    finally:
        adc.close()
        
def plot(df):
    import datetime
    values = list(df['value'])
    datetime = df['datetime']  # .apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    plt.plot(datetime, values)
    plt.xticks(rotation=90)
    
    # ax = plt.gca()
    # xtick_labels = ax.get_xticklabels()
    # print([label.get_text() for label in xtick_labels])
    # new_labels = [pd.Timestamp(label).strftime('%Y-%m-%d %H:%M') for label in datetime]  # 新しいフォーマット
    # ax.set_xticklabels(new_labels, rotation=90)  # ラベルを置き換え    
    
    plt.tight_layout()
    plt.savefig('./plot.png')
    plt.savefig('/var/www/html/cds.png')
    
    plt.close()
    # plt.show()


while True:
    measure(channel=0)
    for _ in tqdm(range(300)):
        time.sleep(1)
