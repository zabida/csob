# coding:utf-8
import Queue
import threading
from sockmqtt import dataTcp_receiver, mqttsvcc_sender
from wizCallHandler import *

sendq = Queue.Queue()  # 该队列通道用于存放从第三方设备子系统采集到的数据
recvq = Queue.Queue()  # 该队列通道用于存放从app端发送的查询或控制的数据


# class win32test(win32serviceutil.ServiceFramework):
#     _svc_name_ = "wizWiseLamp_LINGTEK"
#     _svc_display_name_ = "wizWiseLamp_LINGTEK"
#
#     def __init__(self, args):
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#
#     def SvcDoRun(self):
#         wizWiseLamp_main()
#         win32event.WaitForMultipleObjects(self.hWaitStop, win32event.INFINITE)
#
#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    # 该线程用于从tcp_server端收到的数据存入recvp队列通道中
    t = threading.Thread(target=dataTcp_receiver, args=(recvq,))
    t.start()
    logging.info("mqttsvcc_receiver start---------")
    # 该线程用于从recvq队列通道中获取的data数据进行处理，并放入sendq队列通道
    t = threading.Thread(target=data_recv_handler, args=(recvq, sendq))
    t.start()
    logging.info("query_ctrl start---------")
    # 该线程用于将从从sendq队列通道中获取的处理过的数据发送到wizMqttService
    t = threading.Thread(target=mqttsvcc_sender, args=(sendq,))
    t.start()
    logging.info("mqttsvcc_sender start---------")
    t.join()
