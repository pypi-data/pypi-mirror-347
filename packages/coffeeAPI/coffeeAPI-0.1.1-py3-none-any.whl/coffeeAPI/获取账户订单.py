from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
品种="SHFE.rb2201"
while True:
    #获取总订单
    总订单=api.get_order()
    print(总订单)

    #当已经有订单的时候，找到最前面的订单id
    if 总订单:
        a=[x for x in 总订单][0]

        指定订单=api.get_order(a)
        print(指定订单)

    api.wait_update()

    #如果数据无更新，那么将不会刷新，如果想定时刷新，需要做刷新延迟出来
    #t1=time.time()
    #下面是代表最少0.5秒刷新一次，即使订阅数据无变化
    #api.wait_update(t1+0.5)