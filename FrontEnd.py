import sys
import zmq
import datetime,time

socket_address = "tcp://*:5556"
frontend_name = "FrontEnd01"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(socket_address)

counter = 0
while True:
    status = "GOOD"
    if counter%20==0:
        status = "BAD"
    socket.send_string("%s_*_%s_*_%s" % (frontend_name,status,datetime.datetime.now()))
    counter+=1
    time.sleep(1)


