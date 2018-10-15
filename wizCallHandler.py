# coding:utf-8
import sys
import datetime
import json
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

print sys.getdefaultencoding()

log_file = "./wizCall.log"
logging.basicConfig(filename=log_file, level=logging.INFO)


def client():
    pass


# 该函数用于根据第三方设备Id获取该设备的运行参数，并将数据发送到sendq队列通道中，DataType=QREPLY
def readOnePointInfo(sendq, data, data_dict, req):
    for device in group_devices:
        for doc in data_dict:
            if doc["Info"]["DeviceId"] == device["deviceIotID"]:
                msg = {
                    "SubSys": data["SubSys"],
                    "Version": data["Version"],
                    "Vendor": data["Vendor"],
                    "SysCode": data["SysCode"],
                    "Info": {
                        "Id": doc["Info"]["Id"],
                        "DataType": "QREPLY",
                        "MsgId": req["Info"]["MsgId"],
                        "DeviceStatus": device["lineStatus"],
                        "DeviceName": device["deviceName"],
                        "OnOff": device["switchStatus"],
                        "Brightness": device["brightness"],
                        "Voltage": device["voltage"],
                        "CurrentLevel": device["currentLevel"],
                        "Datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                }
                logging.info("The read one point is %s" % str(msg))
                try:
                    sendq.put(msg)
                    print(7, "put success")
                except Exception as e:
                    logging.info(e.message)


# 该函数用于从recvq队列通道中获取app发送来的查询或是控制命令
def data_recv_handler(recvq, sendq):
    while True:
        # try:
        #     msg = recvq.get()           # 目前postman过来get的是字典
        #     print(1, msg)
        # except Exception as e:
        #     logging.exception(e)
        try:
            msg = recvq.get()
            print(1, msg)
        except Exception as e:
            logging.exception(e.message)
        else:
            if msg:
                # msg = json.dumps(msg)       # 字典转json
                try:
                    req = json.loads(msg)  # json转字典
                    print(req)
                except:
                    print("报错了")
                else:
                    readOnePointInfo(sendq, req)
