import pandas as pd 
import json
from tqsdk.tafunc import time_to_str
import time
import numpy
import asyncio
import websockets
import uuid
import copy
import sys
import traceback
import pandas
import re
import whfunc
class MyDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__




day="day"
night="night"




配置信息={'DCE.eg': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.ZC': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 100.0, 0.2, 1), 'SHFE.ag': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "26:30:00"]]}, 15.0, 1.0, 0), 'SHFE.bu': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 2.0, 0), 'DCE.a': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CFFEX.IH': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:00:00"]], "night": []}, 300.0, 0.2, 1), 'CZCE.MA': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CFFEX.TS': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:15:00"]], "night": []}, 20000.0, 0.005, 3), 'SHFE.zn': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 5.0, 0), 'CZCE.FG': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 20.0, 1.0, 0), 'CZCE.OI': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.SF': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 5.0, 2.0, 0), 'CFFEX.T': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:15:00"]], "night": []}, 10000.0, 0.005, 3), 'DCE.rr': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'DCE.p': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 2.0, 0), 'SHFE.rb': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.PM': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 50.0, 1.0, 0), 'DCE.c': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'DCE.jd': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 10.0, 1.0, 0), 'DCE.cs': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'DCE.pp': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 1.0, 0), 'DCE.jm': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 60.0, 0.5, 1), 'SHFE.hc': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.CF': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 5.0, 0), 'CFFEX.IC': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:00:00"]], "night": []}, 200.0, 0.2, 1), 'CZCE.AP': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 10.0, 1.0, 0), 'SHFE.au': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "26:30:00"]]}, 1000.0, 0.02, 2), 'CZCE.SM': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 5.0, 2.0, 0), 'DCE.lh': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 16.0, 5.0, 0), 'INE.sc': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "26:30:00"]]}, 1000.0, 0.1, 1), 'DCE.m': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.SR': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'SHFE.ru': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 5.0, 0), 'CZCE.SA': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 20.0, 1.0, 0), 'INE.lu': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.PK': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 5.0, 2.0, 0), 'CZCE.JR': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 20.0, 1.0, 0), 'CZCE.TA': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 2.0, 0), 'CZCE.RS': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 10.0, 1.0, 0), 'SHFE.ni': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 1.0, 10.0, 0), 'DCE.pg': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 20.0, 1.0, 0), 'CFFEX.IF': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:00:00"]], "night": []}, 300.0, 0.2, 1), 'CZCE.RI': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 20.0, 1.0, 0), 'DCE.l': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 5.0, 0), 'CFFEX.TF': ({"day": [["09:30:00", "11:30:00"], ["13:00:00", "15:15:00"]], "night": []}, 10000.0, 0.005, 3), 'CZCE.UR': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 20.0, 1.0, 0), 'DCE.eb': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 1.0, 0), 'SHFE.wr': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 10.0, 1.0, 0), 'DCE.fb': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 10.0, 0.5, 1), 'SHFE.ss': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 5.0, 0), 'DCE.b': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.RM': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'SHFE.al': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 5.0, 0), 'CZCE.CJ': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 5.0, 5.0, 0), 'DCE.i': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 100.0, 0.5, 1), 'SHFE.sp': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 2.0, 0), 'INE.nr': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 5.0, 0), 'CZCE.WH': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 20.0, 1.0, 0), 'CZCE.CY': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 5.0, 0), 'DCE.v': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 5.0, 0), 'DCE.y': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 2.0, 0), 'SHFE.fu': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 10.0, 1.0, 0), 'CZCE.LR': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 20.0, 1.0, 0), 'SHFE.pb': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 5.0, 0), 'SHFE.cu': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 10.0, 0), 'DCE.bb': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": []}, 500.0, 0.05, 2), 'DCE.j': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 100.0, 0.5, 1), 'INE.bc': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 5.0, 10.0, 0), 'SHFE.sn': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "25:00:00"]]}, 1.0, 10.0, 0), 'CZCE.PF': ({"day": [["09:00:00", "10:15:00"], ["10:30:00", "11:30:00"], ["13:30:00", "15:00:00"]], "night": [["21:00:00", "23:00:00"]]}, 5.0, 2.0, 0)}


class  GaoApi(object):
    
    def __init__(self,user=None,password=None,loop=None,行情连接地址="ws://127.0.0.1:5252",交易连接地址='ws://127.0.0.1:8765'):
        if loop:
            self.loop=loop
        else:
            self.loop=asyncio.SelectorEventLoop() 


        self.data_base=配置信息
        self.简称映射到交易所={  x.split(".")[1]: x.split(".")[0] for x in 配置信息}

        #判断对象是否改变
        self.cache_obj={}
        self._整体行情更新={}
        self._单品行情更新={}
        self._行情={}
        self._temp_q={}
        self.增加任务=[]
        self.异步连接=None
        self.user=user
        self.password=password
        self.connect_path_md=行情连接地址
        self.connect_path=交易连接地址
        self.保证金={}
        self.手续费={}
        self.更新持仓盈亏=0
        self.断开=0
        #持仓
        self.position={}
        #报单
        self.order={}
        #成交
        self.trade={}
        #资金
        self.account=MyDict()
        self.启动=0
        self.my_websocket=""
        self.my_websocket_md=""
        self.loop.create_task(self.connect_rd())
        self.loop.create_task(self.connect_rd_md())
        
        self.loop.run_forever()
        self.启动=1
    def 初始化行情订阅(self):
        for x in self._行情:
            关键索引=x
            self.增加任务.append(self.get_data_subsription(关键索引.split("_")[0],int(关键索引.split("_")[1]),int(关键索引.split("_")[2])))
        for x in self._temp_q:
            self.增加任务.append(self.get_data_subsription2(x))
    async def  connect_rd_md(self):
        while True:
            try:
                初始化连接=1
                async with websockets.connect(self.connect_path_md) as websocket:
                    self.my_websocket_md=websocket
                    await websocket.send(json.dumps({"user":"000001"}))
                    s=""
                    while True:
                        a=await websocket.recv()
                        #print(a)
                        s=s+a
                        if a[-5:]!="@gao@":
                            continue
                        if 初始化连接 and self.启动:
                            初始化连接=None
                            self.初始化行情订阅()
                            
                        t1=time.time()
                        a=s[:-5]
                        s=""
                        #print(a)
                        #a=a.replace("nan","numpy.nan").replace("1.7976931348623157e+308","numpy.nan").replace("null","numpy.nan").replace("NaN","numpy.nan")
                        if a[:4]=="@ok@":
                            错误=""
                            返回类型,返回参数,返回内容=  a[4:].split("@l@")
                            # print(a)
                            # print(666,返回类型,666)
                            返回类型=json.loads(返回类型)
                            返回参数=json.loads(返回参数)
                            返回内容=[ json.loads(x)  for x in 返回内容.split("^")]
                        else:

                            json_data=json.loads(a)
                            错误=json_data["error"]
                            返回类型=json_data["respond"]
                            返回参数=json_data["parameter"]
                            返回内容=json_data["data"]
                            #json_data=eval(a)
                        if 错误:
                            print(错误)
                            raise Exception(错误)
                        else:
                            if 返回类型=="subsription":
                                关键索引="_".join([ str(x) for x  in 返回参数])
                                数据长度=len(返回内容)
                                需求长度=返回参数[-1]
                                周期=返回参数[-2]
                                #print(关键索引,"haha",数据长度,需求长度)
                                if 数据长度==需求长度:
                                    #print("周期",周期)
                                    if 周期:
                                        self._行情[关键索引]=pandas.DataFrame(返回内容,columns=["datetime","id","open","high","low","close","volume","open_oi","close_oi","symbol","duration"])
                                        # print(关键索引)
                                        # print(self._行情[关键索引])
                                    else:
                                        #print(返回内容)
                                        self._行情[关键索引]=pandas.DataFrame(返回内容,columns=["datetime","id","last_price","average","highest","lowest",
                                        "ask_price1","ask_volume1","bid_price1","bid_volume1",
                                        "ask_price2","ask_volume2","bid_price2","bid_volume2",
                                        "ask_price3","ask_volume3","bid_price3","bid_volume3",
                                        "ask_price4","ask_volume4","bid_price4","bid_volume4",
                                        "ask_price5","ask_volume5","bid_price5","bid_volume5",
                                        "volume","amount","open_interest","symbol","duration"])
                            elif 返回类型=="subsription2":
                                #数据=返回内容
                                品种,UpdateTime, UpdateMillisec, TradingDay,ActionDay,\
                                    LastPrice, Volume, AskPrice1,AskVolume1,BidPrice1,\
                                        BidVolume1,OpenInterest,PreSettlementPrice,PreClosePrice, PreOpenInterest,\
                                OpenPrice,HighestPrice,LowestPrice,Turnover,ClosePrice,\
                                    SettlementPrice,UpperLimitPrice,LowerLimitPrice,BidPrice2,BidVolume2,\
                                        AskPrice2,AskVolume2,BidPrice3,BidVolume3,AskPrice3,\
                                AskVolume3,BidPrice4,BidVolume4,AskPrice4,AskVolume4,BidPrice5,BidVolume5,AskPrice5,AskVolume5,\
                                AveragePrice,volume_multiple,price_tick=返回内容
                                
                                #品种名字=返回参数
                                if 返回参数 not in self._temp_q:
                                    参数tem=返回参数.replace("SP ","")
                                    品种类别=re.findall('[a-zA-Z]{1,}\.[a-zA-Z]{1,}', 参数tem)[0]
                                    self._temp_q[返回参数]=MyDict({
                                    "datetime":"".join([time_to_str(time.time())[:10],' '+UpdateTime+"."+str(UpdateMillisec)]),
                                    "ask_price1":AskPrice1,
                                    "ask_volume1":AskVolume1,
                                    "bid_price1":BidPrice1,
                                    "bid_volume1":BidVolume1,

                                    "ask_price2":AskPrice2,
                                    "ask_volume2":AskVolume2,
                                    "bid_price2":BidPrice2,
                                    "bid_volume2":BidVolume2,

                                    "ask_price3":AskPrice3,
                                    "ask_volume3":AskVolume3,
                                    "bid_price3":BidPrice3,
                                    "bid_volume3":BidVolume3,

                                    "ask_price4":AskPrice4,
                                    "ask_volume4":AskVolume4,
                                    "bid_price4":BidPrice4,
                                    "bid_volume4":BidVolume4,

                                    "ask_price5":AskPrice5,
                                    "ask_volume5":AskVolume5,
                                    "bid_price5":BidPrice5,
                                    "bid_volume5":BidVolume5,

                                    "last_price":LastPrice,
                                    "highest":HighestPrice,
                                    "lowest":LowestPrice,
                                    'open':OpenPrice,
                                    "close":ClosePrice,

                                    'average':AveragePrice,
                                    'volume':Volume,
                                    "amount":Turnover,
                                    "open_interest":OpenInterest,
                                    "settlement":SettlementPrice,
                                    "upper_limit":UpperLimitPrice,
                                    "lower_limit":LowerLimitPrice,
                                    'pre_open_interest':PreOpenInterest,
                                    "pre_settlement":PreSettlementPrice,
                                    "pre_close":PreClosePrice,

                                    "price_tick":price_tick,
                                    "price_decs":self.data_base[品种类别][3],
                                    "volume_multiple":volume_multiple,
                                    "trading_time":self.data_base[品种类别][0],

                                    }
                                    )


                                




                            elif 返回类型=="update_td":
                                品种=''
                                if "k" in 返回内容:
                                    for x in 返回内容["k"]:
                                        品种=x[-2]
                                        #print(x)
                                        关键索引前半段=x[-2]+"_"+str(x[-1])+"_"
                                        长度=len(关键索引前半段)
                                        for y in self._行情:
                                            if y[:长度]==关键索引前半段:
                                                最后时间=self._行情[y].datetime.iloc[-1]
                                                if 最后时间==x[0]:
                                                    self._行情[y].iloc[-1]=x
                                                else:
                                                    self._行情[y].update(self._行情[y].shift(-1))
                                                    self._行情[y].iloc[-1]=x
                                if "q"  in 返回内容:
                                    合约简称,UpdateTime, UpdateMillisec, TradingDay,ActionDay,\
                                    LastPrice, Volume, AskPrice1,AskVolume1,BidPrice1,\
                                    BidVolume1,OpenInterest,PreSettlementPrice,PreClosePrice, PreOpenInterest,\
                                    OpenPrice,HighestPrice,LowestPrice,Turnover,ClosePrice,\
                                    SettlementPrice,UpperLimitPrice,LowerLimitPrice,BidPrice2,BidVolume2,\
                                        AskPrice2,AskVolume2,BidPrice3,BidVolume3,AskPrice3,\
                                    AskVolume3,BidPrice4,BidVolume4,AskPrice4,AskVolume4,\
                                        BidPrice5,BidVolume5,AskPrice5,AskVolume5,AveragePrice=返回内容['q']

                                    #print(666,品种,UpdateTime, UpdateMillisec)
                                    if not 品种:
                                        try:
                                            参数tem=合约简称.replace("SP ","")
                                            temp1=re.findall("[a-zA-Z]{1,}",参数tem)[0]
                                            品种= self.简称映射到交易所[temp1]+"."+合约简称
                                        except:
                                            print(合约简称)
                                    if 品种 in self._temp_q:
                                        self._temp_q[品种].update(
                                        {
                                        "datetime":"".join([time_to_str(time.time())[:10],' '+UpdateTime+"."+str(UpdateMillisec)]),
                                        "ask_price1":AskPrice1,
                                        "ask_volume1":AskVolume1,
                                        "bid_price1":BidPrice1,
                                        "bid_volume1":BidVolume1,

                                        "ask_price2":AskPrice2,
                                        "ask_volume2":AskVolume2,
                                        "bid_price2":BidPrice2,
                                        "bid_volume2":BidVolume2,

                                        "ask_price3":AskPrice3,
                                        "ask_volume3":AskVolume3,
                                        "bid_price3":BidPrice3,
                                        "bid_volume3":BidVolume3,

                                        "ask_price4":AskPrice4,
                                        "ask_volume4":AskVolume4,
                                        "bid_price4":BidPrice4,
                                        "bid_volume4":BidVolume4,

                                        "ask_price5":AskPrice5,
                                        "ask_volume5":AskVolume5,
                                        "bid_price5":BidPrice5,
                                        "bid_volume5":BidVolume5,

                                        "last_price":LastPrice,
                                        "highest":HighestPrice,
                                        "lowest":LowestPrice,
                                        'open':OpenPrice,
                                        "close":ClosePrice,

                                        'average':AveragePrice,
                                        'volume':Volume,
                                        "amount":Turnover,
                                        "open_interest":OpenInterest,
                                        "settlement":SettlementPrice,
                                        "upper_limit":UpperLimitPrice,
                                        "lower_limit":LowerLimitPrice,
                                        'pre_open_interest':PreOpenInterest,
                                        "pre_settlement":PreSettlementPrice,
                                        "pre_close":PreClosePrice,
                                        }
                                        )


                            elif 返回类型=="user":
                                print(返回参数,"行情登陆成功")
                                #continue
                                #初始化连接=1
                            # t2=time.time()
                            # print(t2-t1)
                        #如果更新持仓盈亏为真,订阅行情,并且计算持仓,盈亏,更新维护资金字段






                        #self.loop.stop()
                        if self.my_websocket :
                            self.loop.stop()
            except:
                if self.断开==1:
                    return
                traceback.print_exc()
                print("断开重连")
                time.sleep(5)
    async def  connect_rd(self):
        while True:
            try:
                async with websockets.connect(self.connect_path) as websocket:
                    self.my_websocket=websocket
                    await websocket.send(str({"user":self.user,"password":self.password}))
                    s=""
                    while True:
                        a=await websocket.recv()
                        s=s+a
                        if a[-5:]!="@gao@":
                            continue
                        a=s[:-5]
                        s=""
                        if "逗" in a:
                            raise Exception("密码错误")
                        a=eval(a.replace("nan","numpy.nan").replace("1.7976931348623157e+308","numpy.nan"))
                        #print(a)
                        if "Refresh" in a:
                            self.order.clear()
                            self.trade.clear()
                            self.position.clear()
                        for x in a:
                            if x=="msg":
                                print(a["msg"])
                            if x=="order":
                                if not a[x]:
                                    self.order.clear()
                                    continue
                                for y in a[x]:
                                    if y not in self.order:
                                        self.order[y]=MyDict(a[x][y])
                                    else:
                                        self.order[y].update(a[x][y])
                                # self.order.update(a[x])
                            if x=="trade":
                                if not a[x]:
                                    self.trade.clear()
                                    continue
                                for y in a[x]:
                                    if y not in self.trade:
                                        self.trade[y]=MyDict(a[x][y])
                                    else:
                                        self.trade[y].update(a[x][y])
                            if x=="position":
                                for y in a[x]:
                                    if y not in self.position:
                                        self.position[y]=MyDict(a[x][y])
                                    else:
                                        self.position[y].update(a[x][y])
                                # self.position.update(a[x])
                            if x=="account":
                                self.account.update(a[x])

                            if x=="手续费":
                                self.手续费.update(a[x])
                            if x=="保证金":
                                self.保证金.update(a[x])

                        if self.my_websocket_md:
                            self.loop.stop()
            except:
                if self.断开==1:
                    return
                traceback.print_exc()
                print("断开重连")
                time.sleep(5)
    async def order_add(self,md5,symbol,direction,offset,volume,limit_price,advanced):
        d={"rq":"order_insert","md5":str(md5),"symbol":str(symbol),"direction":str(direction),"offset":str(offset),"volume":int(volume),"price":float(limit_price),"advanced":str(advanced)}
        await self.my_websocket.send(str(d))
    async def commission_add(self,symbol):
        d={"rq":"get_commission","symbol":str(symbol)}
        await self.my_websocket.send(str(d))
    def get_commission(self,symbol):
        if symbol  in self.手续费:
            return self.手续费[symbol]
        self.增加任务.append(self.commission_add(symbol))
        while True:
            if symbol  in self.手续费:
                return self.手续费[symbol]
            self.wait_update()
    async def margin_add(self,symbol):
        d={"rq":"get_margin","symbol":str(symbol)}
        await self.my_websocket.send(str(d))
    def get_margin(self,symbol):
        if symbol  in self.保证金:
            return self.保证金[symbol]
        self.增加任务.append(self.margin_add(symbol))
        while True:
            if symbol  in self.保证金:
                return self.保证金[symbol]
            self.wait_update()

    def insert_order(self, symbol: str, direction: str, offset: str, volume: int, limit_price:float = None,
                    advanced:str = "GFD"):
        if advanced not in ("GFD","FAK","FOK"):
            print("报单类型不支持")
            return
        id =uuid.uuid4().hex
        if limit_price==None:
            if direction=="BUY":
                limit_price=self.get_quote(symbol)["upper_limit"]
            else:
                limit_price=self.get_quote(symbol)["lower_limit"]


        self.增加任务.append(self.order_add(id,symbol,direction,offset,volume,limit_price,advanced))
        self.order[id]=MyDict({
                    "order_id":id,
                    "exchange_order_id":"",
                    "instrument_id":symbol.split(".")[1],
                    "direction": direction,
                    "offset": offset,
                    "volume_orign":volume,
                    "volume_left":volume,
                    "limit_price":limit_price,
                    "price_type":  "LIMIT"  ,
                    "volume_condition": "ANY" if advanced in ("GFD","FAK") else "ALL" ,
                    "time_condition":  "GFD" if advanced=="GFD" else "IOC",
                    "insert_date_time":0,
                    "last_msg":"",
                    "CTP_status": "",
                    "status":    "ALIVE" ,
                    "trade_price":numpy.nan,
                    "trade_records":{}
        })
        return self.order[id]
    def 下单(self,品种,买卖方向,开平方向,下单量,价格=None,下单类型="GFD"):
        if 买卖方向=="买":
            买卖方向="BUY"
        elif 买卖方向=="卖":
            买卖方向="SELL"
        if 开平方向=="开":
            开平方向="OPEN"
        elif 开平方向=="平":
            开平方向="CLOSE"
        elif 开平方向=="平今":
            开平方向="CloseToday"
        self.insert_order(品种,买卖方向,开平方向,下单量,价格,下单类型)
    def create_task(self, coro: asyncio.coroutine) -> asyncio.Task:
        """
        创建一个task

        一个task就是一个协程，task的调度是在 wait_update 函数中完成的，如果代码从来没有调用 wait_update，则task也得不到执行

        Args:
            coro (coroutine):  需要创建的协程

        Example::

            # 一个简单的task
            import asyncio
            from tqsdk import TqApi, TqAuth

            async def hello():
                await asyncio.sleep(3)
                print("hello world")

            api = TqApi(auth=TqAuth("信易账户", "账户密码"))
            api.create_task(hello())
            while True:
                api.wait_update()

            #以上代码将在3秒后输出
            hello world
        """
        #task = self.loop.create_task(coro)
        #if asyncio.Task.current_task(loop=self.loop) is None:
        self.增加任务.append(coro)
        #     task.add_done_callback(self._on_task_done)
        # return task
    async def close_order(self,md5):
        d={"rq":"order_close", "md5":str(md5),}
        await self.my_websocket.send(str(d))
    def _on_task_done(self, task):
        """当由 api 维护的 task 执行完成后取出运行中遇到的例外并停止 ioloop"""
        try:
            exception = task.exception()
            if exception:
                #self._exceptions.append(exception)
                pass
        except asyncio.CancelledError:
            pass
        finally:
            self.增加任务.remove(task)
            self.loop.stop()
    def cancel_order(self, orderid:str) -> None:
        self.增加任务.append(self.close_order(orderid))
    def 撤单(self,订单编号):
        self.cancel_order(订单编号)

    def get_account(self):
        持仓=self.get_position()
        浮动盈亏=0
        持仓盈亏=0
        交易日内平仓盈亏=0
        # 冻结保证金=0
        # 保证金占用=0
        # 冻结手续费=0
        for x in  持仓:
            浮动盈亏+=持仓[x].float_profit
            持仓盈亏+=持仓[x].position_profit
            if "CloseProfit" in 持仓[x]:
                交易日内平仓盈亏+=持仓[x].CloseProfit

        self.account.float_profit=浮动盈亏
        self.account.position_profit=持仓盈亏
        self.account.close_profit=交易日内平仓盈亏
        self.account.balance=self.account.static_balance+持仓盈亏+交易日内平仓盈亏-self.account.commission
        self.account.available=self.account.balance-self.account.frozen_margin-self.account.margin
        return self.account
    
    def 查资金(self):
        return self.account
    def get_order(self,order_id=None):
        if order_id is None:
            return self.order
        else:
            if order_id in self.order:
                return self.order[order_id]
            else:
                return None
    def 查订单(self,订单号=None):
        return self.get_order(订单号)

    def get_trade(self,trade_id=None):
        if trade_id is None:
            return self.trade
        else:
            if trade_id in self.trade:
                return self.trade[trade_id]
            else:
                return None
    def 查成交(self,成交号=None):
        return self.get_trade(成交号)
        
    def get_position(self,symbol=None):
        if symbol is None:
            for x in self.position:
                self.get_quote(x)
                多头浮盈=0
                空头浮盈=0
                多头持仓盈亏=0
                空头持仓盈亏=0
                价格=self._temp_q[x].last_price
                if not numpy.isnan(价格):

                    if self.position[x].pos_long>0:
                        多头浮盈=(价格-self.position[x].open_price_long)*self.position[x].pos_long*self._temp_q[x].volume_multiple
                        if self.position[x].position_price_long!=0:
                            多头持仓盈亏=(价格-self.position[x].position_price_long)*self.position[x].pos_long*self._temp_q[x].volume_multiple
                    if self.position[x].pos_short>0:
                        空头浮盈=(self.position[x].open_price_short-价格)*self.position[x].pos_short*self._temp_q[x].volume_multiple
                        if self.position[x].position_price_short!=0:
                            空头持仓盈亏=(self.position[x].position_price_short-价格)*self.position[x].pos_short*self._temp_q[x].volume_multiple
                    self.position[x].float_profit_long=多头浮盈
                    self.position[x].float_profit_short=空头浮盈
                    self.position[x].float_profit=多头浮盈+空头浮盈
                    self.position[x].position_profit_long=多头持仓盈亏
                    self.position[x].position_profit_short=空头持仓盈亏
                    self.position[x].position_profit=多头持仓盈亏+空头持仓盈亏

            return self.position
        else:
 
            if symbol in self.position:
                x=symbol
                self.get_quote(symbol)
                多头浮盈=0
                空头浮盈=0
                多头持仓盈亏=0
                空头持仓盈亏=0
                价格=self._temp_q[x].last_price
                if self.position[x].pos_long>0:
                    多头浮盈=(价格-self.position[x].open_price_long)*self.position[x].pos_long*self._temp_q[x].volume_multiple
                    多头持仓盈亏=(价格-self.position[x].position_price_long)*self.position[x].pos_long*self._temp_q[x].volume_multiple
                if self.position[x].pos_short>0:
                    空头浮盈=(self.position[x].open_price_short-价格)*self.position[x].pos_short*self._temp_q[x].volume_multiple
                    空头持仓盈亏=(self.position[x].position_price_short-价格)*self.position[x].pos_short*self._temp_q[x].volume_multiple
                self.position[x].float_profit_long=多头浮盈
                self.position[x].float_profit_short=空头浮盈
                self.position[x].float_profit=多头浮盈+空头浮盈
                self.position[x].position_profit_long=多头持仓盈亏
                self.position[x].position_profit_short=空头持仓盈亏
                self.position[x].position_profit=多头持仓盈亏+空头持仓盈亏
                return self.position[symbol]
            else:
                #print("bz")
                #MyDict()
                self.position[symbol]=MyDict()
                a={"exchange_id":symbol.split(".")[0],
                "instrument_id":symbol.split(".")[1],
                'pos_long_his':0,
                "pos_long_today":0,
                "pos_short_his":0,
                "pos_short_today":0,
                "open_price_long":0,
                "open_price_short":0,
                "position_price_long":0,
                "position_price_short":0,
                "position_cost_long":0,
                "position_cost_short":0,
                "float_profit_long":0,
                "float_profit_short":0,
                "float_profit":0,
                "position_profit_long":0,
                "position_profit_short":0,
                "position_profit":0,
                "margin_long":0,
                "margin_short":0,
                'margin':0,
                "pos":0,
                "pos_long":0,
                "pos_short":0,
                "volume_long_frozen_today":0,
                "volume_long_frozen_his":0,
                "volume_short_frozen_today":0,
                "volume_short_frozen_his":0,
                "OpenCost_long_today":0,
                "OpenCost_long_his":0,
                "PositionCost_long_today":0,
                "PositionCost_long_his":0,
                "margin_long_today":0,
                "margin_long_his":0,
                "OpenCost_short_today":0,
                "OpenCost_short_his":0,
                "PositionCost_short_today":0,
                "PositionCost_short_his":0,
                "margin_short_today":0,
                "margin_short_his":0,
                "volume_long_frozen":0,
                "volume_short_frozen":0,
                }
                self.position[symbol].update(a)
                return self.position[symbol]
    def 查持仓(self,品种=None):
        return self.get_position(品种)

    # async def 单symbol更新K任务(self,symbol):
    #     if self.异步连接 is None:
    #         self.异步连接 = await aioredis.create_redis_pool((self.data库连接地址, self.端口),db=self.data库数字,password=self.data库密码,loop=self.loop)
    #     ch1 = await self.异步连接.subscribe(symbol)
    #     ch1=ch1[0]
    #     async def reader(channel):
    #         async for message in channel.iter():
    #             data= eval(message.decode().replace("nan","numpy.nan").replace("1.7976931348623157e+308","numpy.nan"))
    #             #print(data)
    #             for x in self._单品行情更新[symbol]:
    #                 if x =="quote":
    #                     self._单品行情更新[symbol][x].update(data['q'])
    #                     if symbol in self.position:
    #                         if self.position[symbol]["pos_long"]>0:
    #                             self.position[symbol]["float_profit_long"]= ((data['q']["last_price"]-self.position[symbol]["open_price_long"])*self.position[symbol]["pos_long"])*data['q']["volume_multiple"]
    #                         if self.position[symbol]["pos_short"]>0:
    #                             self.position[symbol]["float_profit_short"]= ((self.position[symbol]["open_price_short"]-data['q']["last_price"])*self.position[symbol]["pos_short"])*data['q']["volume_multiple"]
    #                         if self.position[symbol]["pos_long"] or self.position[symbol]["pos_short"]:
    #                             self.position[symbol]["float_profit"]=self.position[symbol]["float_profit_long"]+self.position[symbol]["float_profit_short"]
    #                 else:
    #                     周期=int(x.split("_")[0])
    #                     if self._单品行情更新[symbol][x].datetime.iloc[-1]!=data['k'][周期][0]:
    #                         self._单品行情更新[symbol][x].update(self._单品行情更新[symbol][x].shift(-1))
    #                     #     if 周期:
    #                     #         self._单品行情更新[symbol][x].iloc[-1]=data['k'][周期]+self._单品行情更新[symbol][x].iloc[-1][9:].tolist()
    #                     #     else:
    #                     #         self._单品行情更新[symbol][x].iloc[-1]=data['k'][周期]+self._单品行情更新[symbol][x].iloc[-1][9:].tolist()

    #                     # else:
    #                         #self._单品行情更新[symbol][x].iloc[-1]=data['k'][周期]

    #                     if 周期:
    #                         self._单品行情更新[symbol][x].iloc[-1]=data['k'][周期]+self._单品行情更新[symbol][x].iloc[-1][9:].tolist()
    #                     else:
    #                         self._单品行情更新[symbol][x].iloc[-1]=data['k'][周期]+self._单品行情更新[symbol][x].iloc[-1][7:].tolist()
    #             self.loop.stop()
    #     await reader(ch1)
    
    # async def 全symbol更新K任务(self):
    #     if self.异步连接 is None:
    #         self.异步连接 = await aioredis.create_redis_pool((self.data库连接地址, self.端口),db=self.data库数字,password=self.data库密码,loop=self.loop)
    #     ch1 = await self.异步连接.subscribe(self.订阅推送)
    #     ch1=ch1[0]

    #     async def reader(channel):
    #         async for message in channel.iter():
    #             if not self._整体行情更新:
    #                 continue
    #             data= eval(message.decode().replace("nan","numpy.nan").replace("1.7976931348623157e+308","numpy.nan"))
    #             for y in self._整体行情更新:
    #                 #先拿到symbol
    #                 for x in self._整体行情更新[y]:
    #                     if x =="quote":
    #                         self._整体行情更新[y][x].update(data['q'])
    #                     else:
    #                         周期=int(x.split("_")[0])
    #                         if self._整体行情更新[y][x].datetime.iloc[-1]!=data[y]['k'][周期][0]:
    #                             self._整体行情更新[y][x].update(self._整体行情更新[y][x].shift(-1))
    #                             #self._整体行情更新[y][x].iloc[-1]=data[y]['k'][周期]

    #                         if 周期:
    #                             self._整体行情更新[y][x].iloc[-1]=data[y]['k'][周期]+self._整体行情更新[y][x].iloc[-1][9:].tolist()
    #                         else:
    #                             self._整体行情更新[y][x].iloc[-1]=data[y]['k'][周期]+self._整体行情更新[y][x].iloc[-1][7:].tolist()
    #             self.loop.stop()
    #     await reader(ch1)


    def _set_wait_timeout(self):
        self._wait_timeout = True
        self.loop.stop()



    def wait_update(self,deadline=None):


        deadline_handle = None if deadline is None else self.loop.call_later(max(0, deadline - time.time()),
                                                                              self._set_wait_timeout)
        while True:
            if self.增加任务:
                self.loop.create_task( self.增加任务.pop())
            else:
                break

        self.loop.run_forever()
        if deadline_handle:
            deadline_handle.cancel()

    async def get_data_subsription(self,symbol,周期,长度):
        d={'subsription':[symbol,周期,长度]}
        await self.my_websocket_md.send(json.dumps(d))

    async def get_data_subsription2(self,symbol):
        d={ 'subsription2':symbol}
        await self.my_websocket_md.send(json.dumps(d))

    def get_kline_serial(self,symbol,周期,长度=200):
        关键索引="_".join((symbol,str(周期),str(长度)))
        if 关键索引 in self._行情:
            return self._行情[关键索引]
        else:
             self.增加任务.append(self.get_data_subsription(symbol,周期,长度))
             while True:
                 self.wait_update()
                 #print(666)
                 #print("关键索引",关键索引,"self._行情:",[ x for x in self._行情])
                 if  关键索引 in self._行情:
                     return self._行情[关键索引]

            



        #self.增加任务.append(self.close_order(orderid))
        # if str(周期)+str("_")+str(长度) in self._整体行情更新[symbol]:
        #     return self._整体行情更新[symbol][str(周期)+str("_")+str(长度)]

        # if symbol in self._整体行情更新 and 接受通信方式=="全体":
        #     if str(周期)+str("_")+str(长度) in self._整体行情更新[symbol]:
        #         return self._整体行情更新[symbol][str(周期)+str("_")+str(长度)]
        # if symbol in self._单品行情更新 and 接受通信方式!="全体":
        #     if str(周期)+str("_")+str(长度) in self._单品行情更新[symbol]:
        #         return self._单品行情更新[symbol][str(周期)+str("_")+str(长度)]

        # a= self.red.lrange(symbol+str(周期),0,长度-1)
        # if a:
        #     b=[json.loads(x.decode()) for x in a[::-1] ]
        # else:
        #     b=[]
        # if len(b)<长度:
        #     c=[[0,0,0,0,0,0,0,0,0] for x in range(长度-len(b)) ]
        #     b=c+b
        # c=pd.DataFrame(b,columns=["datetime",'id','open',"high","low",'close','volume',"open_oi","close_oi"]) 
        # if 接受通信方式=="全体":
        #     if symbol not in self._整体行情更新:
        #         self._整体行情更新[symbol]={}
        #     self._整体行情更新[symbol].update({str(周期)+str("_")+str(长度):c})
        # else:
        #     if symbol not in self._单品行情更新:
        #         self.增加任务.append(self.单symbol更新K任务(symbol))

        #         self._单品行情更新[symbol]={}
        #     self._单品行情更新[symbol].update({str(周期)+str("_")+str(长度):c})  
            
        return c

    def 获取_K线(self,品种,周期,长度=200):
        return self.get_kline_serial(品种,周期,长度)


    def get_tick_serial(self,symbol,长度=200):

        关键索引="_".join((symbol,str(0),str(长度)))
        if 关键索引 in self._行情:
            return self._行情[关键索引]
        else:
             self.增加任务.append(self.get_data_subsription(symbol,0,长度))
             while True:
                 self.wait_update()
                 if  关键索引 in self._行情:
                     return self._行情[关键索引]

 
    def 获取_tick线(self,品种,长度=200):
        return self.get_tick_serial(品种,长度)


    def get_quote(self,symbol,接受通信方式="单体"):
        if symbol not in self._temp_q:
             self.增加任务.append(self.get_data_subsription2(symbol))
             while True:
                 self.wait_update()
                 if  symbol in self._temp_q:
                     return self._temp_q[symbol]

        
        else:
            return self._temp_q[symbol]
    def _run_once(self):
        """执行 ioloop 直到 ioloop.stop 被调用"""
        if not self._exceptions:
            self._loop.run_forever()
        if self._exceptions:
            raise self._exceptions.pop(0)
    def close(self):
        self.断开=1
        for task in self.增加任务:
            task.cancel()
        #print(1)
        while self.增加任务:  # 等待 task 执行完成
            self._run_once()
        #print(2)
        # self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()
        #print(3)



    def 获取_tick(self,品种,更新方式="单体"):
        return self.get_quote(品种,更新方式)


    def is_changing(self,对象,对象名字):
        if 对象名字 not in self.cache_obj:
            self.cache_obj[对象名字]= copy.deepcopy(对象)
            return True
        else:
            if 对象!=self.cache_obj[对象名字]:
                self.cache_obj[对象名字]= copy.deepcopy(对象)
                return True
            else:
                return False
    def 判断对象是否改变(self,对象,对象名字):
        return self.is_changing(对象,对象名字)
    
    def 查询当日成交订单(self,品种名=None,保存csv地址="成交记录导出.csv"):
        f=open(保存csv地址,'w')
        f.write("成交时间,成交品种,下单方向,开平标志,委托价格,成交价格,成交手数,委托单号,成交单号\n")
        #f.write()
        if 品种名:
            for x in self.trade:
                b=self.get_trade(x)
                c=self.get_order(b.order_id)
                #print(b)
                if b["instrument_id"]==品种名.split(".")[1]:
                    f.write(','.join([time_to_str(b.trade_date_time),
                    b.instrument_id,
                    b.direction,
                    b.offset,
                    str(c.limit_price),
                    str(b.price),
                    str(b.volume),
                    b.order_id,
                    b.trade_id
                    ])+'\n'
                    )

        else:
            for x in self.trade:
                b=self.get_trade(x)
                #获取成交的订单信息
                c=self.get_order(b.order_id)
                f.write(','.join([time_to_str(b.trade_date_time),
                b.instrument_id,
                b.direction,
                b.offset,
                str(c.limit_price),
                str(b.price),
                str(b.volume),
                b.order_id,
                b.trade_id
                ])+'\n'
                )
        f.close()



if __name__ == "__main__":

    #api=GaoApi("086644","123456",行情连接地址='ws://113.31.102.223:5252')
    api=GaoApi("zhuz04","888888",行情连接地址='ws://124.160.66.119:41253')
    print(1)
    #a=api.get_kline_serial("SHFE.ni2107",0)
    a=api.get_quote("SHFE.ni2108")
    print(2)
    while True: 
        # print(time_to_str(time.time()))
        print(a)
        #print(time_to_str(a.datetime))
        api.wait_update()

        持仓=api.get_position("SHFE.ni2108")
        print(持仓)
        # print(time_to_str(a.datetime.iloc[-1]))

    # mid=0
    # n=0
    # api=GaoApi('040123','123456')
    # a=api.get_kline_serial('SHFE.rb2101',10)
    # while True:
    #     t1=time.time()
    #     api.wait_update(t1+5)
    #     持仓=api.get_position("SHFE.cu2010")
    #     if n==0:
    #         b=api.insert_order("SHFE.cu2010","BUY","CLOSE",1)
    #         n=1
        # if api.is_changing(持仓["pos"],"持仓数量"):
        #print("多仓",持仓["pos_long"],"空仓",持仓["pos_short"])
            # ma5=ma(a.close,5)
            # ma10=ma(a.close,10)
            # print(time_to_str(a.datetime.iloc[-1]),持仓["pos_long"],"上穿",crossup(ma5,ma10).iloc[-2],"下穿",crossup(ma10,ma5).iloc[-2])
            # if crossup(ma5,ma10).iloc[-2] and 持仓["pos_long"]==0:
            #     api.insert_order("SHFE.rb2101","BUY","OPEN",1)
            # if crossup(ma10,ma5).iloc[-2] and 持仓["pos_long"]>0:
            #     api.insert_order("SHFE.rb2101","SELL","CLOSETODAY",1)
        #     if n==0:
        #         b=api.insert_order("SHFE.rb2101","BUY","OPEN",1,3450)
        # print(b)
        # print(api.get_order(b["order_id"]))
        #     n+=1
        # if n==5:
        #     api.cancel_order(b["order_id"])
        # a=api.get_order()
        # for x in a:
        #     if a[x]["volume_left"]==0:
        #         print(a[x])

