from space_comm import receiver
import time


class bs_receiver(receiver):
    def listen_single_msg(self):
        self.waiting = True
        while self.waiting:
            time.sleep(0.1)
        message = list(self.msg)

        return bytes(message)

    def scan_msg(self, msg):
        if msg[1] == 0:
            print(
                "Message has been accepted from the spacecraft with id -> "
                + str(msg[0])
            )
        else:
            print(
                "Message has NOT been accepted from the spacecraft with id -> "
                + str(msg[0])
            )
        return msg


base_station_rcvr = bs_receiver("base_station", False)
spacecraft_msg = base_station_rcvr.listen_single_msg()
spacecraft_msg = base_station_rcvr.scan_msg(spacecraft_msg)
