import sys
import zmq
import datetime,time

socket_address = "tcp://localhost:5566"

im_name = "IM-GLOBAL"
if isinstance(im_name, bytes):
    im_name = im_name.decode('ascii')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(socket_address)
socket.setsockopt_string(zmq.SUBSCRIBE,im_name)

while True:
    msg = socket.recv_string()
    print "%s received at %s" %(msg,datetime.datetime.now())


