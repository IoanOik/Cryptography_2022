from operator import mod
from string import ascii_letters
import string
from space_comm import transmitter
import hashlib
import hmac
import random

t = transmitter("base station")

id = int(input("Give id: "))
dir = int(input("Give direction [1-4] 1-U, 2-R, 3-D, 4-L: "))
dis = int(input("Give dinstance [1-4]: "))

msg_type = 1  # command
pos_x = 10
pos_y = 10

#just deleted here my old freq fail func ,giorgos 


## handle outgoing message
def prepare_msg(msg_type, id, dir, dis):
    key = "secret"
    msg = bytes([msg_type, id, dir, dis])
    mac = hmac.new(bytes(key, "utf-8"), bytes(str(msg), "utf-8"), hashlib.sha256)
    sig = mac.hexdigest()
    freq = 0.6 #the frequency of the msg to BE safe !! FINAL!!
    rand = random.randint(0,10) 
    corrupt=0
   
    if(rand>freq*10):
       corrupt=1

    
    print("rand=" +str(rand)+" freq= "+ str(10*freq) +" ||| corrupt= "+ str(corrupt))
    
    file = open("station.txt", "a")
    file.write("\n"+"Signature made: " + sig )
    file.write(str(msg + bytes(sig, "utf-8")))
    file.close()
    return msg + bytes(sig, "utf-8")
    # return bytes(str([msg_type, id, dir, dis, sig]), 'utf-8')


b = prepare_msg(msg_type, id, dir, dis)
t.transmit(b)
# subprocess.call("./listen_ack.py " + str(id), shell=True)
# args = ["listen_ack.py", str(id)]
# os.execvp("/home/giannis/Documents/cryptography/eclass/Project_01/crypto2022/listen_ack.py", args)
# sys.argv = [str(id)]
exec(open("./listen_ack.py").read())

#exec(open("cd /home/project ; /usr/bin/env /bin/python3 /root/.vscode-server/extensions/ms-python.python-2022.4.1/pythonFiles/lib/python/debugpy/launcher 45741 -- /home/project/Cryptography_2022/base_station.py ").read())
