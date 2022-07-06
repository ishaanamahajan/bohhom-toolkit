<h1 style="font-size:7vw">LOCOBOT WX250s</h1>


  
  <p1>This is a tutorial to get the locobot moving by setting up a navigation point towards which the locobot navigates itself by avoiding obstacles or by using the arrow keys on your laptop, which in this case, the robot would be fully in manual control. </p1>

<h2 style="font-size:3vw">Requisites</h2>

  <p2 >A few requisites to ssh into locobot: 
  <ol>
  <li>Ubuntu 18.04 or higher</li>
  <li>ROS1 or ROS2 (the version will depend upon what ubuntu version you are running)</li>
  <li>Rviz (for simulation)</li>
</ol></p2>

<h3 style="font-size:3vw">Entering the workspace</h3>
  <p3> Make sure the locobot computer and your computer are connected to the same wifi network before proceeding. 
  <br> Use the command <code>ssh -X locobot@< ipaddress of the locobot computer></code> (The -X command allows window formatting which will be useful while running tests in simulation). Now enter the command <code>/usr/bin/dbus-launch /usr/bin/gnome-terminal &</code> to open a new terminal.</p3>

<h4 style="font-size:3vw">Moving the robot</h4>
  <p4> First, we need to setup SLAM. We can start one from scratch by using the command <code> roslaunch interbotix_xslocobot_nav xslocobot_nav.launch robot_model:=locobot_wx200 use_lidar:=true rtabmap_args:=-d </code>. Remeber to change the robot model accordingly. To start up simulation in rviz, you can use the command <code> roslaunch interbotix_xslocobot_descriptions remote_view.launch rviz_frame:=map</code>. There are two ways to move the robot: 
  <ol>
  <li><code>roslaunch interbotix_xslocobot_joy xslocobot_joy.launch robot_model:=locobot_wx200 launch_driver:=false</code>. When using this command, you need to set up a end destination in Rviz using the 2D Nav Goal button. The command will help the robot navigate to the location you set in simulation along with obstacle detection.</li>
  <li><code>roslaunch kobuki_keyop keyop.launch __ns:=locobot</code>. This command will help you navigate/move the robot using your keyboard arrow keys. Please note : While using this method, the robot will be in complete manual mode, therefore there will be no obstacle detection.</li>
</ol></p4>

<h5 style="font-size:3vw">NLP</h5>
  <p5>To operate the robot on human voice commands, we need to run three things at the same time. Activate the virtual environment first in home directory by running the command <code>source py37_env.sh</code>. It can be deactivated using the command <code>deactivate</code>. Then in the first terminal window, run the launch file  <code>roslaunch interbotix_xslocobot_control xslocobot_control.launch robot_model:=locobot_wx250s use_base:=true use_camera:=true use_lidar:=true</code>. In the second terminal window run the command <code> rosrun jrh_test jrh_test_control_MB.py </code>. In the third terminal window, run the command <code> rosrun jrh_test jrh_ subscriber.py</code>.</p5>

<h6 style="font-size:3vw">Help and Support</h6>
   <p6> For help running the locobot wx250s based in NUS, contact the Controls and Simulation Lab </p6>


   




