import sys
import zmq
import datetime,time

socket_address = "tcp://localhost:5566"

bpm_name = "BPM-GLOBAL"
if isinstance(bpm_name, bytes):
    bpm_name = bpm_name.decode('ascii')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(socket_address)
socket.setsockopt_string(zmq.SUBSCRIBE,bpm_name)

while True:
    msg = socket.recv_string()
    print msg


