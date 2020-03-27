#!/usr/bin/env python

import rospy
import time
from uuid import uuid4
from std_msgs.msg import String
import os
from std_srvs.srv import Empty, EmptyResponse
from kompose_manager.srv import Uuid, UuidResponse
from datetime import datetime
import threading

def server(req):
    print(req)
    s = 'data: {}'.format(req.uuid)
    print('Got call doing work... with {}'.format(s))
    print(os.getcwd()+'/test.txt')
    with open(os.getcwd()+'/test.txt', 'w+') as f:
        f.write(s)
    rospy.loginfo(s)
    return UuidResponse()

def start_server():
    s = rospy.Service('server', Uuid, server)
    rospy.spin()

def client():
    try:
        rospy.wait_for_service('server')
        server_proxy_func = rospy.ServiceProxy('server', Uuid)
        rate = rospy.Rate(0.5)
        while not rospy.is_shutdown():
            resp = server_proxy_func(str(uuid4()))
            rate.sleep()
    except rospy.ServiceException, e:
        print "Service call failed: {}".format(e)
    

if __name__ == '__main__':
    try:
        rospy.init_node('server_client', anonymous=True)
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        client()
        server_thread.join()
    except rospy.ROSInterruptException:
        pass