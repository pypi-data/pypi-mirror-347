from gaoapi import GaoApi
import time

#api=GaoApi("086644","123456",行情连接地址="ws://119.3.87.93:5252")
#api=GaoApi("086644","123456",行情连接地址="ws://110.40.184.104:5252")
api=GaoApi("086644","086644",行情连接地址="ws://110.40.184.104:5253")
品种="DCE.i2201"
#行情=api.get_kline_serial(品种,30*60,200)
#行情=api.get_kline_serial(品种,60,10)
# 品种="CZCE.AP201"
# 行情t=api.get_quote(品种)
print(5)
保证金=api.get_margin("SHFE.rb2201")
print(保证金)
# 保证金=api.get_commission("SHFE.rb2201")
# print(保证金)
# #print(行情)
# print(行情t)
# 品种1="DCE.SP i2110&i2111"
# 行情t1=api.get_quote(品种1)
#print(行情)
#行情=api.get_tick_serial(品种,5)
#print(行情t1)
# 持仓=api.get_position("SHFE.rb2201")
# #委托=api.get_order()
# 订单=api.insert_order("SHFE.rb2201","BUY","OPEN",10,5400)
# #资金=api.get_account()
n=0
while True:
    #print(行情)
    # print(行情t)
    # print(time.time())
    # 持仓=api.get_position("SHFE.rb2201")
    # print(持仓)
    # 资金=api.get_account()
    # print(资金)
    # 订单=api.get_order()
    # print(len([x for x in 订单]))
    #print(持仓.pos_long)
    #print(资金)
    # # print(行情)
    # print(委托)
    # for x in 委托:
    #     订单=api.get_order(x)
    #     if 订单.status=="ALIVE":
    #         api.cancel_order(订单.order_id)
    api.wait_update()
    # n+=1
    # if n>20:
    #     api.close()
    #     break
    
    # #print(行情)
    # print(行情t)
#     # print(行情t1)
# api=GaoApi("086622","123456",行情连接地址="ws://127.0.0.1:5253")
# 行情t=api.get_quote(品种)
# # #print(行情)
# # print(行情t)
# # 品种1="DCE.SP i2110&i2111"
# # 行情t1=api.get_quote(品种1)
# #print(行情)
# # 行情=api.get_tick_serial(品种,50)
# #print(行情t1)
# 持仓=api.get_position("SHFE.rb2201")
# #委托=api.get_order()
# #订单=api.insert_order("SHFE.rb2201","BUY","OPEN",10,5500)
# #资金=api.get_account()
# n=0
# while True:
#     print(n)
#     print(持仓)
#     api.wait_update()
#     n+=1
