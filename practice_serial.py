import rospy
import serial
import struct
import tf
from geometry_msgs.msg import Pose
class device:
    pass;



def serial_connection(port='/dev/ttyACM0'):

    ser = serial.Serial(port, 15200)
    print("im here")



    data = ser.read_until("ok\n")


    april_tag_num = int(struct.unpack("f", data[0:4])[0])

    tag_dict = dict()
    counter = 4
    for tag in range(april_tag_num):

        current_tag_ = "tag" + str(tag)
        tag_dict[current_tag_] = {}
        tag_dict[current_tag_]["tag_id"], tag_dict[current_tag_]["x_translation"], \
        tag_dict[current_tag_]["y_translation"], tag_dict[current_tag_]["z_translation"], \
        tag_dict[current_tag_]["x_rotation"], tag_dict[current_tag_]["y_rotation"], \
        tag_dict[current_tag_]["z_rotation"] = struct.unpack("7f", data[counter: counter + 28])
        counter +=28
        print tag_dict[current_tag_]
    #for april_tag in tag_dict:
        #myPose = Pose()
        #myPose.position.x, myPose.position.y, myPose.position.z, myPose.orientation.x, myPose.orientation.y, \
        #myPose.orientation.z, myPose.orientation.w = ADD corresponding values here after quaternion calculations

def handle_pose(msg, args):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.position.x, msg.position.y, msg.position.z),
                     (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w),
                     rospy.Time.now(),
                     args[0],
                     args[1])
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
        if not mydevice.is_connected:
            try:
                serial_connection()
            except rospy.ROSInterruptException:
                quit(-1)
        else:
            pass;