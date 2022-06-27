**Sim_Helper**
==============

This module simulates various path finding algorithms through virtual quadcopter and turtlebot agents.


**Setting Up The Simulation**
-----------------------------

- To adjust the number of simulated vehicles modify the `./launch/launch_sim.launch` file.  Changing the `spawn_turtles` argument enables/disables the list of turtlebots.

- To switch between the two basic modes of flying (basic waypoints and Dubins path) change the `waypointmode` argument.  Default behavior is `True` which starts the basic waypoints algorithm.


**Running The Simulation**
--------------------------

- In one terminal run `python scripts/Master.py`.

- Wait a few seconds until __Autopilot ARMED__ and __RC override active__ are printed and then in another terminal run `roslaunch sim_estimator.launch` from the launch directory.

- If the simulation is set to run the setpoint generator code, wait until __Takeoff!__ is printed in the second terminal and then use `rosparam set /setpoint_publisher/active true` if you are using the setpoint_generator to start the simulated quadcopter.  Use `rosparam set /setpoint_publisher/active false` to signal the quadcopter to head back to the origin.
Otherwise, if you are using dubins path, use `rosparam set /setpoint_publisher/activaction false` to launch it.


