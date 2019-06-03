#!/usr/bin/ env python

import rospy
import math
from geometry_msgs.msg import Pose
from std_msgs.msg import String

cycles = 0
my_pose = Pose()
my_pose.position.x=1
my_pose.position.y=1

my_pose.orientation.x = 0
my_pose.orientation.y = 0
my_pose.orientation.z = 0
my_pose.orientation.w = 1


rospy.init_node('sine_wave', anonymous=True)
pub = rospy.Publisher('sine', Pose, queue_size=10)

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    cycles += 1
    my_pose.position.z = math.sin(cycles)
    pub.publish(my_pose)
    rate.sleep()
    rospy.loginfo_throttle(5, 'heartbeat')