#!/usr/bin/env python

import rospy
import time
from uuid import uuid4
from std_msgs.msg import String

import threading

def callback(data):
    s = rospy.get_caller_id() + " I'm talker and I heard  {}".format(data.data)
    rospy.loginfo(s)

def talker():
    pub = rospy.Publisher('foo', String, queue_size=10)
    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        hello_str = str(uuid4())
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

def listener():
    rospy.Subscriber('foo', String, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        talker_thread = threading.Thread(target=talker)
        listener_thread = threading.Thread(target=listener)
        talker_thread.start()
        listener_thread.start()
        listener_thread.join()
        talker_thread.join()
    except rospy.ROSInterruptException:
        pass