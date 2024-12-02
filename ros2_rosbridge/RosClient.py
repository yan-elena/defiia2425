#!/usr/bin/env python
# Authors: Badeig 

import json
import threading
import websocket
import time

class RosClient():
    """
    class RosClient provides a simple API to interact with ROS2 environment throught the websocket rosbridge
    """

    def __init__(self, ip, port):
        """
        Contruct an object RosClient
        :param self:
        :param ip: the IP of the rosbridge
        :type ip: str
        :param port: the port of the rosbridge
        :type port: int
        :return:
        """
        self._url = ip+':'+ str(port) 
        """information about websocket rosbridge composed of the ip and the port"""
        self._topics = []
        """list of the topic subscription"""
        self._services = []
        """list of the current service calls (waiting the service response)"""
        self._messageBox = [] 
        """list of the received messages including subscription and service response"""
        self._connected = False
        """status of the connection with the rosbridge"""

    def connect(self):
        """
        Connect to the rosbridge and launch in detached process the subscription management to receive the messages
        :param self:
        :return:
        """
        # websocket.enableTrace(True)
        self._websocket = websocket.WebSocket()
        self._websocket.connect('ws://'+self._url)
        self._connected = True
        thread = threading.Thread(target=self.on_listen)
        thread.start()

    def disconnect(self):
        """
        Wait the end of services calls, unsubscribe to record topics and disconnect from rosbridge
        :param self:
        :return:
        """
        while self._services:
            time.sleep(2.0)
        while self._topics:
            elt = self._topics[0]
            self.unsubscribe(elt) #unscribe all topics and then discuonect
        self._websocket.close()

    def on_listen(self):
        """
        process to manage subscriptions to receive the messages
        Update the message box of the client
        :param self:
        :return:
        """
        while self._connected:
            try:
                message = json.loads(self._websocket.recv())
                print('[received]: '+str(message))
                if 'topic' in message and message['topic'] in self._topics :
                    self._messageBox.append(message) #if is on the list, i store, if not
                    continue
                if 'service' in message and message['service'] in self._services :
                    self._messageBox.append(message)
                    self._services.remove(message['service'])
                    continue
            except:
                break        

    def publish(self, topic, value):
        """
        process to manage subscriptions to receive the messages
        Update the message box of the client
        :param self:
        :param topic: the topic on ros
        :type str:
        :param value: the message to publish
        :type json:
        :return:
        """
        message = { "op": "publish", "topic": topic, "msg": value }
        self._websocket.send(json.dumps(message))
    
    def subscribe(self, topic, type):   
        """
        subscription to a specific topic
        Update the topics list of the client
        :param self:
        :param topic: the topic on ros
        :type str:
        :param typee: the type of the topic (ros type)
        :type str:
        :return:
        """
        message = {"op": "subscribe", "topic": topic, "type": type}
        self._websocket.send(json.dumps(message))
        if not (topic in self._topics) :
            self._topics.append(topic)

    def unsubscribe(self, topic):
        """
        Unsubscription to a specific topic on ros and remove the information on the topics list
        :param self:
        :param topic: the topic on ros
        :type str:
        :return:
        """     
        message = {"op": "unsubscribe", "topic": topic}
        self._websocket.send(json.dumps(message))
        self._topics.remove(topic)

    def advertise(self, topic, type):     
        """
        Declaration of intent to interact on a specific topic on ros
        :param self:
        :param topic: the topic on ros
        :type str:
        :param type: the message to publish
        :type str:
        :return:
        """
        message = {"op": "advertise", "topic": topic, "type": type}
        self._websocket.send(json.dumps(message))
        
    def unadvertise(self, topic, type):     
        """
        Declaration of intent to interact on a specific topic on ros
        :param self:
        :param topic: the topic on ros
        :type str:
        :param type: the message to publish
        :type str:
        :return:
        """
        message = {"op": "unadvertise", "topic": topic, "type": type}
        self._websocket.send(json.dumps(message))
        
    def call_service(self, name, args=None): #call services on the other node?
        """
        process to manage subscriptions to receive the messages
        Update the message box of the client
        :param self:
        :param name: the name of the service
        :type str:
        :param args: the list of parameters to run the service
        :type list:
        :return:
        """
        if not args:     
            message = {"op": "call_service", "service": name}
        else:
            message = {"op": "call_service", "service": name, "args": args}
            print(message)
        self._websocket.send(json.dumps(message))
        if not (name in self._services) :
            self._services.append(name)

    def getTopics(self):
        """
        Request a specific API of rosbridge to get the list of existing topics on ROS environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/topics")

    def getServices(self):
        """
        Request a specific API of rosbridge to get the list of existing services on ROS environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/services")

    def getNodes(self):
        """
        Request a specific API of rosbridge to get the list of existing nodes  on ROS environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/nodes")

#  (optional) "args": <list<json>>,
#  (optional) "fragment_size": <int>,
#  (optional) "compression": <string>

# main 
def main():    
    myclient = RosClient('localhost', 9090) 
    myclient.connect()   
    myclient.subscribe("/turtle1/cmd_vel", "geometry_msgs/Twist")
    time.sleep(3) 
    myclient.publish("/turtle1/cmd_vel", {'linear': {'x': 4.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 6.3}})
    time.sleep(3) 
    # myclient.getTopics()
    # myclient.getServices()
    # myclient.getNodes()
    myclient.call_service('/turtle1/teleport_absolute', args=[5.0, 10.0, 3.0])
    
if __name__ == '__main__':
    main()
