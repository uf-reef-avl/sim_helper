**Sim_Helper**
==============

This module simulates various path finding algorithms through virtual quadcopter and turtlebot agents.

**Setting Up The Simulation**
-----------------------------
1. Clone PX4 Firmware 

   ```bash
   cd ~
   git clone https://github.com/PX4/Firmware.git --recursive
   cd ~/Firmware
   ```
1. Install [PX4 dependencies](http://dev.px4.io/en/setup/dev_env_linux_ubuntu.html#common-dependencies). 
   ```bash
   # Install PX4 "common" dependencies.
   ./Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx
   ```
1. Build Firmware
   ```bash
   # Build and run simulation
   make px4_sitl_default gazebo
   # Ctrl+C after Gazebo opens
   ```
1. Source "launch_common.sh" (Do this every time on first launch)
    ```bash
    source ~/catkin_ws/src/reef_estimator_sim_bundle/sim_helper/launch/launch_common.sh
    # you may have to adjust this path and launch_common.sh to fit your directories
    ```

- To adjust the number of simulated vehicles modify the `launch/launch_sim.launch` file.  Changing the `spawn_turtles` argument enables/disables the list of turtlebots.

- To switch between the two basic modes of flying (basic waypoints and Dubins path) change the `waypointmode` argument.  Default behavior is `True` which starts the basic waypoints algorithm.


**Running The Simulation**
--------------------------

- In one terminal run `python scripts/Master.py -i px4`.
- In another terminal run `roslaunch sim_helper px4_sim_est_control.launch`
- If the simulation is set to run the setpoint generator code, wait until __Takeoff!__ is printed in the second terminal and then use `rosparam set /setpoint_publisher/active true` if you are using the setpoint_generator to start the simulated quadcopter.  Use `rosparam set /setpoint_publisher/active false` to signal the quadcopter to head back to the origin.
Otherwise, if you are using dubins path, use `rosparam set /setpoint_publisher/activaction false` to launch it.
- In another terminal set PX4 to OFFBOARD mode with `rosservice call /mavros/set_mode "base_mode: 0 custom_mode: 'OFFBOARD'"`
*Note: PX4 Params may have to be set in the included params/px4_sitl.param file through QGC
- To change the IMU Publishing rate (this controls the rate REEF Estimator runs at) use mavlink stream commmands:
   ```mavlink stream -d <telem_port> -s Attitude -r <rate>```
   This can either be done via the mavlink console in QGC, or put into the etc/extras.txt on the Pixhawk

 
