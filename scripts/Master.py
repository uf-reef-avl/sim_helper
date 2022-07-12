#!/usr/bin/env python
# license removed for brevity

import rospy
import rospkg
import roslaunch
import time
import RC_code
import sys
import getopt


def main(argv):

    # Selecting Flight Stack
    flight_stack = "rosflight"
    options = "i:"
    long_options = ["input"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argv, options, long_options) 
    except getopt.GetoptError:
        print('Options:\n -i <flightstack> (rosflight, px4)\n')
        sys.exit(2)
    for opt, arg in arguments:
        if opt == '-i':
            flight_stack = arg 

    # Setting up launch files and nodes #
    rospack = rospkg.RosPack()
    path = rospack.get_path('sim_helper')
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    cli_args = [path + "/launch/launch_sim.launch"]

    # Adding necessary arguments to launch file
    if flight_stack == "px4":
        cli_args.append('px4:=True')

    # Launching Launch file 
    roslaunch_args = cli_args[1:]
    roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
    rotor_launch = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
    rotor_launch.start()
    rospy.loginfo("started")
    rospy.sleep(5.0)
    
    # Launch rosflight (if necessary)
    if flight_stack == "rosflight":
	    node = roslaunch.core.Node(package='rosflight', node_type='rosflight_io', name='rosflight_io', namespace='/', args='_udp:=true', output='screen')
	    flight_launch = roslaunch.scriptapi.ROSLaunch()
	    flight_launch.start()
	    flight_launch.launch(node)
	    rospy.sleep(3.0)

    RC_code.main()

if __name__ == '__main__':
    main(sys.argv[1:])
