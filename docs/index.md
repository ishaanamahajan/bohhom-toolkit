<h1 style="font-size:10vw">LOCOBOT WX250s</h1>


  
  <p1 style ="font-size:2vw">This is a tutorial to get the locobot moving by setting up a navigation point towards which the locobot navigates itself by avoiding obstacles or by using the arrow keys on your laptop, which in this case, the robot would be fully in manual control. </p1>

<h2 style="font-size:5vw">Requisites</h2>

  <p2 >A few requisites to ssh into locobot: 
  <ol>
  <li>Ubuntu 18.04 or higher</li>
  <li>ROS1 or ROS2 (the version will depend upon what ubuntu version you are running)</li>
  <li>Rviz (for simulation)</li>
</ol></p2>

<br><h3 style="font-size:5vw">Entering the locobot workspace</h3>
  <p3> Make sure the locobot computer and your computer are connected to the same wifi network before proceeding. 
  <br> Use the command <code>ssh -X locobot@< ipaddress of the locobot computer></code> (The -X command allows window formatting which will be useful while running tests in simulation). Now enter the command <code>/usr/bin/dbus-launch /usr/bin/gnome-terminal &</code> to open a new terminal.</p3>

<br><h4 style="font-size:5vw">Moving the robot</h3>
  <p4> First, we need to setup SLAM. We can start one from scratch by using the command <code> roslaunch interbotix_xslocobot_nav xslocobot_nav.launch robot_model:=locobot_wx200 use_lidar:=true rtabmap_args:=-d </code>. Remeber to change the robot model accordingly. To start up simulation in rviz, you can use the command <code> roslaunch interbotix_xslocobot_descriptions remote_view.launch rviz_frame:=map</code>. There are two ways to move the robot: 
  <ol>
  <li><code>roslaunch interbotix_xslocobot_joy xslocobot_joy.launch robot_model:=locobot_wx200 launch_driver:=false</code>. When using this command, you need to set up a end destination in Rviz using the 2D Nav Goal button. The command will help the robot navigate to the location you set in simulation along with obstacle detection. 
  <li><code>roslaunch kobuki_keyop keyop.launch __ns:=locobot</code>. This command will help you navigate/move the robot using your keyboard arrow keys. Please note : While using this method, the robot will be in complete manual mode, therefore there will be no obstacle detection.
</ol></p4>


   




