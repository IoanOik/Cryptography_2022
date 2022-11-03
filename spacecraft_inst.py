from space_comm import receiver
from spacecraft import spacecraft
import time,sys
from threading import Thread, Lock


class spacecraft_inst():

    def __init__(self,id,lock):

        task = open("task","r").readline().rstrip("\n")
        if task == '1.3' or task == '1.4':
            comm_failure = True
        else:
            comm_failure = False

        self.s =  spacecraft(id)
        self.r = receiver("spacecraft_"+str(id),comm_failure)
        self.lock = lock

    def launch(self):
        while True:
            time.sleep(0.01)
            msg = self.r.listen_single_msg()
            msg = self.handle_msg(msg)
            self.lock.acquire()
            self.s.process_msg(msg)
            self.lock.release()

    #handle incoming messages
    def handle_msg(self,msg):
        return msg
