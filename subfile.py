#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard %s", data.data)
def listener():
    rospy.init_node('sine_wave')
    rospy.Subscriber('sine', Pose, callback)
    rospy.spin()

if __name__ == "__main__":
    listener()