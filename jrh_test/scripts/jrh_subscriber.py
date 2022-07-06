#!/usr/bin/env python

from logging.config import listen
import rospy
from geometry_msgs.msg import Twist
# from mainz import *
# from utils import predict
import rospy
import time
from std_msgs.msg import Int16




def doMsg(msg):

    
    pub = rospy.Publisher("/locobot/mobile_base/commands/velocity", Twist, queue_size=1000)
    

    #moving forward
    if msg.data == 2:
        
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.1
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            print ("Recieved data")
            pub.publish(msg)
            rate.sleep()

    #moving backward
    elif msg.data == 3:
        
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = -0.1
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            print ("Recieved data")
            pub.publish(msg)
            rate.sleep()


    #turning around (180 degrees)
    elif msg.data == 4:
        
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.628319

        
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            print ("Recieved data")
            pub.publish(msg)
            rate.sleep()


    # turning left
    elif msg.data == 5:
        print (msg.data)
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.4

        
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()

    # turning right
    elif msg.data == 6:
        
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = -0.4

        
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()
    
    # going to location A
    elif msg.data == 7:
        print("message recieved")
        
        # moving forward
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.4
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(8)
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()
        
        # turning left 
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.3

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()
        
        # going straight 
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.6
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(12)
        while (rospy.Time.now() < end):
            pub.publish(msg)
            rate.sleep()
 
       # turning towards location
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = -0.2

        
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        
        while (rospy.Time.now() < end):
            print("Loop entered")
            pub.publish(msg)
            rate.sleep()
    
    #going to exit
    elif msg.data == 8:
        print("message recieved")
        
        # moving forward
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.4
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        start = rospy.Time.now()
        end = start + rospy.Duration(8)
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()
        
        # turning right 
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = -0.2

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(5)
        while (rospy.Time.now() < end):
            
            pub.publish(msg)
            rate.sleep()
        
        # going straight 
        rate = rospy.Rate(10)
        msg = Twist()
        msg.linear.x = 0.4
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        #start = time.time()
        start = rospy.Time.now()
        end = start + rospy.Duration(13)
        while (rospy.Time.now() < end):
            pub.publish(msg)
            rate.sleep()
    

    # if sub == 2 :
    #     rate = rospy.Rate(10)
    #     msg = Twist()
    #     msg.linear.x = 0.5
    #     msg.linear.y = 0.0
    #     msg.linear.z = 0.0
    #     msg.angular.x = 0.0
    #     msg.angular.y = 0.0
    #     msg.angular.z = 0.0

    #     start = time.time()
    #     end = start +3
    #     #while (start< end):
    #     sub.publish(msg)
    #     rospy.spin()
           
    # elif sub == 3 :
    #     rate = rospy.Rate(10)
    #     msg = Twist()
    #     msg.linear.x = -0.5
    #     msg.linear.y = 0.0
    #     msg.linear.z = 0.0
    #     msg.angular.x = 0.0
    #     msg.angular.y = 0.0
    #     msg.angular.z = 0.0



if __name__=="__main__" :
    rospy.init_node("movement")
    
    sub = rospy.Subscriber("jrh_zqw",Int16,doMsg, queue_size=100)
  
        # start = time.time()
        # while (start< start + 3):
        #    sub.publish(msg) 

    
    rospy.spin()
