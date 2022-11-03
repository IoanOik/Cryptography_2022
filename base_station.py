from space_comm import transmitter

t = transmitter('base station')

id = int(input("Give id: "))
dir = int(input("Give direction [1-4] 1-U, 2-R, 3-D, 4-L: "))
dis = int(input("Give dinstance [1-4]: "))

msg_type = 1 # command
pos_x = 10
pos_y = 10


## handle outgoing message
def prepare_msg(msg_type,id,dir,dis):
    return bytes([msg_type,id,dir,dis])

b = prepare_msg(msg_type,id,dir,dis)
t.transmit(b)