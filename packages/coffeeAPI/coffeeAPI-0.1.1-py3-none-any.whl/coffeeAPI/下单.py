from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
品种="SHFE.rb2208"

指定价格=4800
是否已经下单=0
订单id=0
while True:
    if 是否已经下单==0:
        #                品种  买卖方向 开平方向，手数 价格，  下单命令(默认普通下单，可以选FOK或者FAK 需要交易所支持品种)
        订单id=api.insert_order(品种,  "BUY",   "OPEN",  1, 指定价格)
        是否已经下单=1
    api.wait_update()

    #后续可以根据订单Id查询订单状态
    print(订单id)


    #如果数据无更新，那么将不会刷新，如果想定时刷新，需要做刷新延迟出来
    #t1=time.time()
    #下面是代表最少0.5秒刷新一次，即使订阅数据无变化
    #api.wait_update(t1+0.5)