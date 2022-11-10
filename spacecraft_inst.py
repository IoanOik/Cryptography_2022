from ast import If
from space_comm import receiver
from spacecraft import spacecraft
import time, sys
from threading import Thread, Lock
import datetime
import hashlib
import hmac
from space_comm import transmitter


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
        while True:
            time.sleep(0.01)
            msg = self.r.listen_single_msg()
            msg = self.handle_msg(msg)
            self.lock.acquire()
            self.s.process_msg(msg)
            self.lock.release()

    # handle incoming messages
    def handle_msg(self, msg):

        key = "secret"
        mac = hmac.new(
            bytes(key, "utf-8"), bytes(str(msg[:4]), "utf-8"), hashlib.sha256
        )
        caclulated_sig = mac.hexdigest()
        signature = (msg[4:]).decode("utf-8")
        valid = hmac.compare_digest(signature, caclulated_sig)
        ack_message = [
            self.s.id,
            0,
        ]  # init the acknowledgement message as an accepted one
        if len(msg) == 68:
            if valid:
                msg = msg + bytes([1])
                if msg[0] == 1:
                    if msg[1] == self.s.id:
                        self.s.t.transmit_to_ack_topic(
                            bytes(ack_message)
                        )  # transmit that the msg has been accepted by the spacecraft
                        timestamp = str(datetime.datetime.now())
                        direction = str(msg[2])
                        distance = str(msg[3])
                        file = open(str(self.s.id) + ".txt", "a")
                        file.write(
                            "Time: "
                            + timestamp
                            + " Direction: "
                            + direction
                            + " Distance: "
                            + distance
                            + "\n"
                        )
                        file.close()
                        f = open("commands.txt", "a")
                        f.write("The command I got " + str(msg) + str(len(msg)) + "\n")
                        f.close()
            else:
                # the message must be rejected!
                msg = msg + bytes([0])
                ack_message[1] = 1
                self.s.t.transmit_to_ack_topic(
                    bytes(ack_message)
                )  # transmit that the msg has NOT been accepted by the spacecrafts
            message_file = open("Transmitted.txt", "a")
            message_file.write(
                "Id "
                + str(self.s.id)
                + " Message sent: "
                + str(ack_message)
                + " Is Valid: "
                + str(valid)
                + " Is for me: "
                + str(self.s.id == msg[1])
                + "\n"
            )
            message_file.close()
        return msg
