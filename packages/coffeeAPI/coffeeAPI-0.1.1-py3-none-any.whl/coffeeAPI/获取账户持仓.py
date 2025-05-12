from gaoapi import GaoApi
import time
api=GaoApi("086622","123456",行情连接地址="ws://81.68.181.176:5253",交易连接地址="ws://81.68.181.176:8765")
品种="SHFE.rb2201"
while True:
    #获取总持仓
    总持仓=api.get_position()
    print(总持仓)

    指定品种持仓=api.get_position(品种)
    print(指定品种持仓)

    api.wait_update()

    #如果数据无更新，那么将不会刷新，如果想定时刷新，需要做刷新延迟出来
    #t1=time.time()
    #下面是代表最少0.5秒刷新一次，即使订阅数据无变化
    #api.wait_update(t1+0.5)