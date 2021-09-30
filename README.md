**Sim_Helper**
==============

This module simulates the explorer relay through virtual quadcopter and turtlebot agents.

**Install the package:**
--------------------
	
		mkdir -p ~/explorer_relay_ws/src
		cd ~/explorer_relay_ws/src
		git clone http://10.251.72.180/explorer-relay-demo/relay_explorer_bundle.git
		cd relay_explorer_bundle/
		git submodule update --init --recursive
		cd ~/explorer_relay_ws
		catkin build


**Running The Simulation**
--------------------------

- Open 4 terminal

- Source all of them with :

		source ~/explorer_relay_ws/devel/setup.bash


- In the first terminal, launch the simulation:

		cd ~/explorer_relay_ws

		python src/relay_explorer_bundle/sim_helper/scripts/Master.py

- When it is fully launched, send the following command in another terminal, to start the quad:

		roslaunch relay_controller exp_launch.launch

- Then in another terminal launch the quad controller:

		roslaunch relay_controller relay_controller.launch

- At the beginning all the bots move thanks to the gazebo odom topic, use the following line to make them use their estimated positions (launch this command after seeing the log : "Quad give gps" inside the first terminal, it means that the estimator has been updated with at least one gps measurement):

		rosparam set /mode "estimator"



