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
        self._actions = []
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
        while self._actions:
            time.sleep(2.0)
        while self._topics:
            elt = self._topics[0]
            self.unsubscribe(elt)
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
                    self._messageBox.append(message)
                    continue
                if 'service' in message and message['service'] in self._services :
                    self._messageBox.append(message)
                    self._services.remove(message['service'])
                    continue
                if 'action' in message :
                    for elt in self._actions :
                        if elt['action'] == message['action'] and elt['id'] == message['id']:
                            self._messageBox.append(message)
                            if message['op'] == 'action_result' :
                                print(self._actions)
                                self._actions.remove({"action": message['action'], "id": message['id']})
                            continue
            except:
                break        

    def publish(self, topic, value):
        """
        publish a message on the specific topic         
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
        Declaration of unintent to stop to interact on a specific topic on ros
        :param self:
        :param topic: the topic on ros
        :type str:
        :param type: the message to publish
        :type str:
        :return:
        """
        message = {"op": "unadvertise", "topic": topic, "type": type}
        self._websocket.send(json.dumps(message))
        
    def call_service(self, name, args=None):
        """
        process to call an existing service in ROS environment
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
        Request the list of existing topics on ROS environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/topics")

    def getServices(self):
        """
        Request the list of existing services on ROS environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/services")

    def getNodes(self):
        """
        request the list of existing nodes on ros environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/nodes")

    def getTopicInfo(self, topic_name):
        """
        request more details about a topic
        :param self:
	:param topic_name: topic name 
        :return:
        """
        self.call_service("/rosapi/topic_type", args=[topic_name])

    def getServiceInfo(self, service_name):
        """
        request more info about a service
        :param self:
	:param service_name: service name 
        :return:
        """
        self.call_service("/rosapi/service_type", args=[service_name])

    def getServiceInput(self, service_name):
        """
        request information about input type of a service
        :param self:
	:param service_name: service name 
        :return:
        """
        self.call_service("/rosapi/service_request_details", args=[service_name])

    def getServiceOutput(self, service_name):
        """
        request information about output type of a service
        :param self:
	:param service_name: service name 
        :return:
        """
        self.call_service("/rosapi/service_response_details", args=[service_name])


    def getMessageInfo(self, message_type):
        """
        request details about ROS message type
        :param self:
	:param message_type: message type 
        :return:
        """
        self.call_service("/rosapi/message_details", args=[message_name])

    def getNodeDetails(self, node_name):
        """
        request information abour publishers and subscribers of a node
        :param self:
	    :param node_name: node name 
        :return:
        """
        self.call_service("/rosapi/node_details", args=[node_name])

    def getActionServers(self):
        """
        request the list of existing action servers  on ros environment
        :param self:
        :return:
        """
        self.call_service("/rosapi/action_servers")

    def send_goal(self, action, action_type, action_id, args=None):
        """
        send a goal request to an action server
        :param self:
        :param action:
        :param action_type:
        :param action_id:
        :return:
        """
        #message = {"op": "send_action_goal", "action": "turtlebot3move", "action_type": "simple_action_server/action/Turtlebot3Move", "feedback": True, "args": [1.6, "right"]}
        message = {"op": "send_action_goal", "action": action, "action_type": action_type, "id": action_id, "feedback": True, "args": args}
        self._websocket.send(json.dumps(message))
        self._actions.append({"action": action, "id": action_id}) 

    def cancel_goal(self, action, action_id):
        """
        send a cancel request to an action server for a specific action goal
        :param self:
        :param action:
        :param action_id:
        :return:
        """
        #message = {"op": "send_action_goal", "action": "turtlebot3move", "action_type": "simple_action_server/action/Turtlebot3Move", "feedback": True, "args": [1.6, "right"]}
        message = {"op": "cancel_action_goal", "action": action, "id": action_id}
        self._websocket.send(json.dumps(message))

# main 
def main():    
    myclient = RosClient('localhost', 9090) 
    myclient.connect()   
    #myclient.subscribe("/turtle1/cmd_vel", "geometry_msgs/Twist")
    #time.sleep(3) 
    #myclient.publish("/turtle1/cmd_vel", {'linear': {'x': 4.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 6.3}})
    myclient.getTopics()
    # myclient.getServices()
    # myclient.getServiceInput('turtlesim/SetPen')
    # myclient.getServiceInfo('/turtle1/set_pen')
    # myclient.getMessageInfo('geometry_msgs/Twist')
    # myclient.getNodeDetails('/turtlesim')
    # myclient.getActionServers()
    # myclient.call_service('/turtle1/teleport_absolute', args=[5.0, 10.0, 3.0])
    myclient.disconnect()

if __name__ == '__main__':
    main()
