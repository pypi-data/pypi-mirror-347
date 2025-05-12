from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
品种="DCE.i2201"
长度=5
while True:
    #获取tick序列
    #                         品种 ，长度
    行情t=api.get_tick_serial(品种 ,  长度)
    print(行情t)
    api.wait_update()