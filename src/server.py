#!/usr/bin/env python

import rospy
import time
from uuid import uuid4
from std_msgs.msg import String
import os
from std_srvs.srv import Empty, EmptyResponse
from kompose_manager.srv import Uuid, UuidResponse
from datetime import datetime

def server(req):
    print('Got call doing work... with {}'.format(s))
    s = 'data: {}'.format(req.uuid)
    with open(os.getcwd()+'/test.txt', 'w+') as f:
        f.write(s)
    rospy.loginfo(s)
    return UuidResponse()

def start_server():
    s = rospy.Service('server', Uuid, server)
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('server', anonymous=True)
        start_server()
    except rospy.ROSInterruptException:
        pass