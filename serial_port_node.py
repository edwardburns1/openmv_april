#! /usr/bin/env python
import rospy
import serial
import struct
import tf
import numpy
import yaml
from tf import transformations
from geometry_msgs.msg import Pose




class device:
    pass;



def serial_connection(port='/dev/ttyACM0'):

    ser = serial.Serial(port, 15200)
    print("im here")



    data = ser.read_until("ok\n")
    print data

    april_tag_header, april_tag_data = int(struct.unpack("f", data[0:4])[0]) , data[4:]

    tag_dict = dict()
    counter = 0
    for tag in range(april_tag_header):

        current_tag = "tag" + str(tag)
        tag_dict[current_tag] = {}
        current_dict = tag_dict[current_tag]

        current_dict["tag_id"], current_dict["x_translation"], \
        current_dict["y_translation"], current_dict["z_translation"], \
        current_dict["x_rotation"], current_dict["y_rotation"], \
        current_dict["z_rotation"] = struct.unpack("7f", april_tag_data[counter: counter + 28])
        counter +=28

        #current_dict["x_translation"] = -1 * current_dict["x_translation"]
        #current_dict["y_translation"] = -1 * current_dict["y_translation"]
        #current_dict["z_translation"] =  current_dict["z_translation"]
        #print current_dict

        rotation_matrix = transformations.euler_matrix(current_dict["x_translation"], current_dict["y_translation"], current_dict["z_translation"])

        reshaped_matrix = [i[0:3] for i in rotation_matrix][0:3]

        # Fix reshaped list comprehension


        y_rot = numpy.matrix([[0,0,1],[0,1,0],[-1,0,0]])
        rot_about_y = numpy.matmul(reshaped_matrix,y_rot)

        z_rot = numpy.matrix([[0,-1, 0],[1,0,0],[0,0,1]])


        final_rot_matrix = numpy.matmul(rot_about_y, z_rot)





        final_rot_matrix = numpy.hstack((final_rot_matrix, [[0],[0],[0]]))
        final_rot_matrix = numpy.vstack((final_rot_matrix, [0,0,0,1]))
        print final_rot_matrix



        #reshaped_final_rot_matrix = [numpy.append(i, [0], axis=0) for i in final_rot_matrix]


        quaternion = transformations.quaternion_from_matrix(final_rot_matrix)
        #quaternion = transformations.quaternion_from_euler(current_dict["x_rotation"], current_dict["y_rotation"], current_dict["z_rotation"])



        raw_pose = Pose()
        raw_pose.position.x, raw_pose.position.y, raw_pose.position.z, raw_pose.orientation.x, raw_pose.orientation.y, \
        raw_pose.orientation.z, raw_pose.orientation.w = current_dict["x_translation"], current_dict["y_translation"], current_dict["z_translation"], \
        quaternion[0], quaternion[1], quaternion[2], quaternion[3]


        edited_pose = Pose()
        edited_pose.position.x = -1 * raw_pose.position.z
        edited_pose.position.y =  -1 * raw_pose.position.x
        edited_pose.position.z = raw_pose.position.y
        edited_pose.orientation.x = raw_pose.orientation.x
        edited_pose.orientation.y = raw_pose.orientation.y
        edited_pose.orientation.z = raw_pose.orientation.z
        edited_pose.orientation.w = raw_pose.orientation.w
        
        handle_pose(raw_pose, ("camera", "april"+"_" + str(int(current_dict["tag_id"]))))
        handle_pose(edited_pose, ("ROS_edit", "april"+"_" + str(int(current_dict["tag_id"]))))


def handle_pose(msg, args):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.position.x, msg.position.y, msg.position.z),
                     (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w),
                     rospy.Time.now(),
                     args[0],
                     args[1])


if __name__ == '__main__':
    rospy.init_node('serial_connection')

    mydevice = device()
    mydevice.is_connected = False

    while not rospy.is_shutdown():
        rospy.loginfo_throttle(10, "heartbeat...")
        serial_connection()


        



