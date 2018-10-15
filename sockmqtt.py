# coding:utf-8
import socket
import logging
import time
import json
from settings import MQTTSERVICE_HOST, MQTTSERVICE_PORT, DATA_HOST, DATA_PORT, _user, _pwd

logging.basicConfig(level=logging.INFO)
BUFSIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 该函数用于连接socket server端，支持断线重连
def tcp_connect(host, port):
    global s
    while True:
        try:
            logging.info("Trying to connect to mqtt service.")
            s.connect((host, port))
        except socket.error, e:
            logging.exception("Connection error: %s" % e)
            time.sleep(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            logging.info("Connected to mqtt service.")
            return


# 该函数用于从sendq队列通道取出采集到的第三方设备子系统数据，发送给wizMqttService
def mqttsvcc_sender(sendq):
    while True:
        try:
            msg = sendq.get()
        except Exception as e:
            logging.exception(e)
        else:
            if msg:
                try:
                    msg_j = json.dumps(msg)
                except:
                    pass
                else:
                    try:
                        s.sendall(msg_j)
                        logging.info(msg)
                    except Exception as e:
                        logging.exception(e)
                        tcp_connect(MQTTSERVICE_HOST, MQTTSERVICE_PORT)


# 该函数用于将从app端发送来的查询或控制数据存储到recvq队列通道
def dataTcp_receiver(recvq):
    while True:
        try:
            msg = s.recv(BUFSIZE).decode("gbk").encode("utf8")
        except Exception as e:
            logging.exception(e)
            tcp_connect(DATA_HOST, DATA_PORT)
            senddata = "Action: InfCtrLogin\nInfCtrUser: %s\nInfCtrPwd: %s\n\n" % _user, _pwd
            s.send(senddata)
        else:
            if msg:
                try:
                    recvq.put(msg)
                except Exception as e:
                    logging.exception(e)
            else:
                tcp_connect(DATA_HOST, DATA_PORT)
                senddata = "Action: InfCtrLogin\nInfCtrUser: 80004817847300\nInfCtrPwd: J0443120026\n\n"
                s.send(senddata)

# tcp_connect(MQTTSERVICE_HOST, MQTTSERVICE_PORT)
