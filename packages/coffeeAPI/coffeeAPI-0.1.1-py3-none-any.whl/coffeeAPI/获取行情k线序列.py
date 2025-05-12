from gaoapi import GaoApi
import time
api=GaoApi("zhuz04","888888",行情连接地址="ws://127.0.0.1:5253")
品种="DCE.i2208"

#周期是用秒做单位，只能正整数
周期=10
长度=5
while True:
    #获取k序列
    行情=api.get_kline_serial(品种 , 周期, 长度)
    #print(行情)

    行情=api.get_kline_serial(品种 , 60, 3)
    print(行情)

    行情=api.get_kline_serial(品种 , 120, 3)
    print(行情)

    行情=api.get_kline_serial(品种 , 180, 3)
    print(行情)

    api.wait_update()