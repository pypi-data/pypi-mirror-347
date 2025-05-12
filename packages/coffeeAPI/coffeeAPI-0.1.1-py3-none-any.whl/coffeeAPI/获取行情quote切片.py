from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
#品种="DCE.i2201"
品种="DCE.SP l2201&l2205"
while True:
    #获取quote行情
    行情t=api.get_quote(品种)
    print(行情t)
    api.wait_update()