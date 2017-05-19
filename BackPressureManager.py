import sys
import zmq
import datetime,time

recv_socket_address = "tcp://localhost:5556"
send_socket_address = "tcp://*:5566"

frontend_name = "FrontEnd"
if isinstance(frontend_name, bytes):
    frontend_name = frontend_name.decode('ascii')

frontend_dict = { 'INIT':"GOOD" }
current_status = "GOOD"
    
context = zmq.Context()

send_freq_sec = 5
send_socket = context.socket(zmq.PUB)
send_socket.bind(send_socket_address)

recv_socket = context.socket(zmq.SUB)
recv_socket.connect(recv_socket_address)
recv_socket.connect("tcp://localhost:5557")
recv_socket.setsockopt_string(zmq.SUBSCRIBE,frontend_name)

timelast = datetime.datetime.now()
while True:
    msg = recv_socket.recv_string()
    print msg

    msg_list = msg.split("_*_")
    fe = msg_list[0]
    status = msg_list[1]

    frontend_dict[fe] = status
    print("\t%s Status = %s" % (fe,status) )
    if status!=current_status:
        tmp_status="GOOD"
        for stat in frontend_dict.values():
            print "\t\t%s" % stat
            if stat!="GOOD":
                tmp_status="BAD"
                break
        print "TMP_STATUS=%s, GlobalStatus=%s" % (tmp_status,current_status)
        if tmp_status!=current_status:
            current_status=tmp_status
            send_socket.send_string("%s_*_%s_*_%s" % ("BPM-GLOBAL",current_status,datetime.datetime.now()))
            timelast = datetime.datetime.now()
        current_status=tmp_status
    print("\tGlobalStatus = %s" % current_status)
    timenow = datetime.datetime.now()
    diff = timenow - timelast
    if diff.seconds>send_freq_sec:
        send_socket.send_string("%s_*_%s_*_%s" % ("BPM-GLOBAL",current_status,datetime.datetime.now()))
        timelast = timenow

