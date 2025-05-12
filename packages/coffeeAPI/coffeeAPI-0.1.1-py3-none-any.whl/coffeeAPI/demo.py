from tqsdk.tafunc import time_to_str
from gaoapi import GaoApi
#from 实时文华K2 import *
import time
#api=GaoApi("086644","123456",行情连接地址='ws://106.75.245.135:5252')
#api=GaoApi("086644","123456",行情连接地址='ws://119.3.87.93:5253')
api=GaoApi("zhuz04","888888",行情连接地址='ws://124.160.66.119:41253')
#获取tick切片面
#行情=api.get_quote("SHFE.ni2108")
##获取tick序列
#行情=api.get_tick_serial("SHFE.ni2108",10)
##获取K线 序列
品种="SHFE.rb2208"
品种2="SHFE.hc2208"
# 行情=api.get_kline_serial("SHFE.ni2108",60)
#行情=[ api.get_kline_serial(x,60,100) for x in (品种,品种2)]
# 行情2=api.get_kline_serial(品种,86400,200)
# print(行情)
行情t=api.get_quote(品种)
# 行情1=api.get_tick_serial(品种,100)
# # for x in range(100,1,-1):
#     print(x)
#     print(time_to_str(行情.datetime.iloc[-x]))
# #查询持仓
# # 持仓=api.get_position("SHFE.ni2108")
# 历史=数据历史合成(品种,16,(("21:00:00","23:00:00"),),api,3000)

# 实时=实时数据合成(品种,16,(("21:00:00","23:00:00"),),api,历史,50,1000)
# n=0
# def run(行情):
#     pass
while True:
    print(行情t)
    api.wait_update()
#     for x in 行情:
#         run(x)
    #print(行情)
    # print(行情t.datetime)
    # # print(time.time())
    # # print(行情2)
    # print(行情1)
    #print(行情1)
    # print(行情)
    # print("多仓数量",持仓.pos_long)
    # print("空仓数量",持仓.pos_short)
    # print(持仓)
    #实时=实时数据合成(品种,16,(("21:00:00","23:00:00"),),api,历史,50,1000)
    #查委托
    # 总委托=api.get_order()
    # # if n==0:
    # #     n=1
    # #     for x in 总委托:
    # #         委托=api.get_order(x)
    # #         print(委托.instrument_id,"委托时间",time_to_str(委托.insert_date_time),"买卖方向",委托.direction,"开平方向",委托.offset)

    # #下委托
    # if n==0:
    #     n=1
    #     api.insert_order("SHFE.ni210","BUY",'OPEN',2,139300)
    #     print(666)
    #api.wait_update()
    #print(实时)

    # print("....................")
    # 实时2=api.get_kline_serial("SHFE.rb2201",60*16)
    # for x in range(30,0,-1):

    #     print(time_to_str(实时2.datetime.iloc[-x]))
    # print("----------------------")
    api.wait_update()


