from space_comm import receiver
from spacecraft import spacecraft
import time, sys
from threading import Thread, Lock
from base_station_as import Encryptor


class spacecraft_inst:
    def __init__(self, id, lock):
        task = open("task", "r").readline().rstrip("\n")
        if task == "1.3" or task == "1.4":
            comm_failure = True
        else:
            comm_failure = False

        self.s = spacecraft(id)
        self.r = receiver("spacecraft_" + str(id), comm_failure)
        self.lock = lock

    def launch(self):
        self.decryptor = Encryptor(str(self.s.id))
        while True:
            time.sleep(0.01)
            msg = self.r.listen_single_msg()
            msg, valid = self.handle_msg(msg)
            self.lock.acquire()
            self.s.process_msg(msg, valid)
            self.lock.release()

    # handle incoming messages
    def handle_msg(self, msg):
        valid = True
        decrypted_msg = None
        if len(msg) == 544:
            key = open("base_station.txt", "rb").read()
            valid = self.decryptor.verify_signature(cipherText=msg, sender_public_key=key)
            if valid:
                decrypted_msg = self.decryptor._decrypt_(msg)
            return decrypted_msg, valid
        return msg, valid
