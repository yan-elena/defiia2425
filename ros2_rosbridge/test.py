#!/usr/bin/env python
# Authors: Badeig 

import json
import RosClient
import time

# main 
def main():    
    ## WARNING a client 
    myclient = RosClient('localhost', 9090) 
    myclient.connect()   
    myclient2 = RosClient('localhost', 9090) 
    myclient2.connect()   
    #myclient.subscribe("/turtle1/cmd_vel", "geometry_msgs/Twist")
    #time.sleep(3) 
    #myclient.publish("/turtle1/cmd_vel", {'linear': {'x': 4.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 6.3}})
    time.sleep(3) 
    myid = 'turtlebot3Move' + str(2)
    myclient.send_goal("turtlebot3move", "simple_action_server/action/Turtlebot3Move", myid, [3.14, "right"])
    time.sleep(2)
    myclient.getTopics()
    # myclient.getServices()
    # myclient.getServiceInput('turtlesim/SetPen')
    # myclient.getNodeDetails('/turtlesim')
    # myclient.getActionServers()
    # myclient.call_service('/turtle1/teleport_absolute', args=[5.0, 10.0, 3.0])
    time.sleep(2)
    print('send cancel goal')
    myclient2.cancel_goal("turtlebot3Move",myid)
    myid = 'turtlebot3Move' + str(3)
    myclient2.send_goal("turtlebot3move", "simple_action_server/action/Turtlebot3Move", myid, [0.5, "forward"])
    time.sleep(10)
    myclient.disconnect()
    myclient2.disconnect()

    
if __name__ == '__main__':
    main()
