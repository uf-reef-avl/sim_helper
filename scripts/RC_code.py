#!/usr/bin/env python
# license removed for brevity

import rospy
import time
import os
import yaml
from Odometry_to_PoseStamped import odometry_to_posestamped
from frame_conversion import frame_conversion

from mavros_msgs.msg import *
from mavros_msgs.srv import *
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import *

class RC_Code:

    def __init__(self):
        self.current_state = State()
        self.current_pose = PoseStamped()

        # Setup publisher #
        rospy.init_node('RC', anonymous=False)
        self.rc_pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=20)
        self.state_sub = rospy.Subscriber("/mavros/state", State, self.state_cb)
        self.pose_sub = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, self.pose_cb)

        # Setup conversion node #
        otp = odometry_to_posestamped()
        if rospy.get_param("/use_px4_sitl", False):
            frame_conversion()

        # Setup service calls
        arming_client = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        set_mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)


        r = rospy.Rate(50)
        rospy.sleep(2.0)
        last_request = rospy.get_rostime()

        i = 0
        while not rospy.is_shutdown():
            cmd = OverrideRCIn()
            cmd.channels = [1500, 1500, 1500, 1500, 1500, 1500, 2000, 1500,0,0,0,0,0,0,0,0,0,0]
            now = rospy.get_rostime()
            if i < 100:
                pass
            elif self.current_state.mode != "OFFBOARD":
                if self.current_state.armed == False and (now - last_request > rospy.Duration(2)):
                    cmd.channels = [1500, 1500, 1500, 1500, 1500, 1500, 2000, 1500,0,0,0,0,0,0,0,0,0,0]
                    arming_client(True)
                    last_request = now
                elif (self.current_state.mode != 'POSCTL' and self.current_state.mode != 'OFFBOARD') and (now - last_request > rospy.Duration(2)):
                    set_mode_client(base_mode=0, custom_mode="POSCTL")
                    last_request = now
                elif (self.current_state.mode == 'POSCTL' and self.current_state.armed == True):
                    cmd.channels = [self.throttle, 1500, 1500, 1500, 1500, 1500, 2000, 1500,0,0,0,0,0,0,0,0,0,0]
            self.rc_pub.publish(cmd)
            i+=1

            r.sleep()

        rospy.loginfo('RC node has shutdown')
        rospy.signal_shutdown()

    def state_cb(self, msg):
        self.current_state = msg
        
    def pose_cb(self, msg):
        self.current_pose = msg
        self.throttle = 1750 + (1 - self.current_pose.pose.position.z) * 250
        #self.throttle = 1800
def main():
    RC_Code()
if __name__ == '__main__':
    main()
