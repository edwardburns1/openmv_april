#! /usr/bin/env python

import yaml
import rospy
import rosparam
from geometry_msgs.msg import TransformStamped
import tf2_ros

def yaml_read(file):
    with open(file, "r") as stream:
        tag_list = yaml.safe_load(stream)

        while not rospy.is_shutdown():
            for tag in tag_list["tags"]:

                broadcast_static_transform(tag)

def broadcast_static_transform(tag):
    broadcaster = tf2_ros.StaticTransformBroadcaster()

    static = TransformStamped()

    static.header.stamp = rospy.Time.now()
    static.header.frame_id = "world"
    static.child_frame_id = "tag" + str(tag["id"])

    static.transform.translation.x = tag["x"]
    static.transform.translation.y = tag["y"]
    static.transform.translation.z = tag["z"]

    static.transform.rotation.x = tag["qx"]
    static.transform.rotation.y = tag["qy"]
    static.transform.rotation.z = tag["qz"]
    static.transform.rotation.w = tag["qw"]

    print (static)
    broadcaster.sendTransform(static)

if __name__ == "__main__":
    rospy.init_node("static_tag_broadcaster")
    yaml_read(rospy.get_param("yaml_static_file"))