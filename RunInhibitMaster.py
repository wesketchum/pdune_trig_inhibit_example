import zmq
import InhibitMaster

context = zmq.Context()
publisher = InhibitMaster.InhibitPUBNode(context,"tcp://*:5566")

subscriber = InhibitMaster.StatusSUBNode(context)
subscriber.connect("tcp://localhost:5556")
subscriber.connect("tcp://localhost:5557")

im = InhibitMaster.InhibitMaster(0.5,True)

im.run(subscriber,publisher)
