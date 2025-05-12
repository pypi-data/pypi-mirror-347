from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
品种="DCE.i2201"


while True:
    #获取指定品种手续费比例，只能获取普通商品合约的！      套利合约和期权的不能使用！
    手续费比例=api.get_commission(品种)
    print(手续费比例)
    api.wait_update()


    #如果数据无更新，那么将不会刷新，如果想定时刷新，需要做刷新延迟出来
    #t1=time.time()
    #下面是代表最少0.5秒刷新一次，即使订阅数据无变化
    #api.wait_update(t1+0.5)