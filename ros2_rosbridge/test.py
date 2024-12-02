#!/usr/bin/env python
# Authors: Badeig 

import json
import RosClient
import time

# main 
def main():    
    myclient = RosClient.RosClient('localhost', 9090)
    myclient.connect()  

    #tp-basic-operations
    myclient.getTopics() # list the newly created topics 
    myclient.getServices()  #list the newly created topics 
    myclient.subscribe("/turtle1/pose", "turtlesim/Pose")




    myclient.subscribe("/turtle1/cmd_vel", "geometry_msgs/Twist")
    time.sleep(1) 
    myclient.publish("/turtle1/cmd_vel", {'linear': {'x': 4.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 6.3}})
    time.sleep(2) 
    # myclient.getTopics()
    # myclient.getServices()
    # myclient.getNodes()

    #                                               [position x, position y and orientation]
    myclient.call_service('/turtle1/teleport_absolute', args=[5.0, 10.0, 3.0]) 
    time.sleep(2)
    # myclient.unsubscribe("/turtle1/cmd_vel")
    while myclient._messageBox:
        message = myclient._messageBox.pop(0)
        print(message)
    time.sleep(2)
    myclient.disconnect()
    
if __name__ == '__main__':
    main()
