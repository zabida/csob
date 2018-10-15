# coding:utf8
from socket import *

address = '192.168.127.100'
port = 5050
buffsize = 1024
s = socket(AF_INET, SOCK_STREAM)
s.connect((address, port))
senddata = "Action: InfCtrLogin\nInfCtrUser: 80004817847300\nInfCtrPwd: J0443120026\n\n"
s.send(senddata)
while True:
    recvdata = s.recv(buffsize).decode('gbk').encode('utf8')
    a = recvdata.replace("\r\n", '')
    print(a)
s.close()
