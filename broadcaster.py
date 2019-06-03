#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Pose

def handle_pose(msg, args):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.position.x, msg.position.y, msg.position.z),
                     (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w),
                     rospy.Time.now(),
                     args[0],
                     args[1])


if __name__ == '__main__':
    rospy.init_node('sine_wave')
    rospy.Subscriber('sine', Pose, handle_pose, ('map', 'world'))
    rospy.spin()






