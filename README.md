## Spaceship communication system ##
### _Overview_ ###

Welcome to the Spaceship Communication System project! This project aims to simulate the communication system between a base station and multiple spaceships. The system allows the base station  operator to issue commands to spaceships, while the spaceships report back their position to a monitor. 

To get started with the system, please refer to the instructions in the `environment.sh` file and execute it in your terminal. Then, run `monitor.py` to create a space map and show the spacecrafts. You can launch 4 spaceships by executing `launch_spacecrafts.py 4`. Finally, you can send commands to the spaceships by executing `base_station.py`.

The communication between the base station and spaceships is done through bytes arrays, with two types of messages:
- command messages
- reporting messages

The first byte of each message indicates its type, with 0 for reporting messages and 1 for command messages. I hope you find this project informative and enjoyable! If you have any questions or feedback, please feel free to reach out to me.
