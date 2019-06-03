import rospy
import os
import subprocess
import std_msgs.msg
from grbl_motion_control.srv import *
from geometry_msgs.msg import Vector3
import psutil
import signal
rospy.init_node("walker_node")
DIRECTORY = "/home/edward/ws_tracker/src/grbl_motion_control/gcodes"


def search_for_gcode(directory):
    run_list = []
    os.chdir(directory)

    for file in os.listdir(directory):
        if file.endswith(".gcode"):
            run_list.append(file)

    return run_list

def pack_gcode(run_list):
    data = []
    for file in run_list:

        with open(file, 'r') as readfile:
            contents = readfile.read()
        data.append({'path': os.getcwd() + file, 'filename': file, 'contents': contents})
    return data


def motion_control_client(contents):
    rospy.wait_for_service('/motionControl/request')
    try:
        send_gcode = rospy.ServiceProxy('/motionControl/request', GrblMotionRequest)
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        jog_val = Vector3(0.0, 0.0, 0.0)

        send_gcode(header, 3, jog_val, contents)
    except rospy.ServiceException as e:
        print ("Service call failed: %s" %e)


def terminate_process_and_children(p):
    process = psutil.Process(p.pid)
    for sub_process in process.children(recursive=True):
        sub_process.send_signal(signal.SIGINT)
    p.wait()  # we wait for children to terminate


def mail_contents(packed):
    os.chdir("/home/edward/ws_grbl/src/sinepub/bags")
    for dictionary in packed:
        subprocess.Popen(['rosbag', 'record', '-o', dictionary['filename'], '/motionControl/position', '/motionControl/status', '__name:=rosbagger'])
        motion_control_client(dictionary['contents'])

        subprocess.Popen(['rosnode', 'kill', 'rosbagger']).wait()


if __name__ == "__main__":
    run_list = search_for_gcode(DIRECTORY)
    PACKED_GCODE = pack_gcode(run_list)
    mail_contents(PACKED_GCODE)


