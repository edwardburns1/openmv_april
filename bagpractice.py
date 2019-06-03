import subprocess, os, signal
import time
import rospy
def terminate_process_and_children(p):
  import psutil
  process = psutil.Process(p.pid)
  for sub_process in process.children(recursive=True):
      sub_process.send_signal(signal.SIGINT)
  p.wait()  # we wait for children to terminate


os.chdir("/home/edward/ws_grbl/src/sinepub/bags")
for number in ['a', 'b']:
    rosbag_proc = subprocess.Popen(['rosbag', 'record', '-o', number, '/motionControl/position', '__name:=checker'])

    time.sleep(4)

    #terminate_process_and_children(rosbag_proc)

    subprocess.Popen(['rosnode', 'kill', 'checker']).wait()


