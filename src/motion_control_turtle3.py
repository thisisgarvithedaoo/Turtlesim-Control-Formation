#!/usr/bin/env python3

import turtlesim.srv
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

def posecallback3(msg):
    global pose
    pose = msg

def goalcallback3(msg):
    global goal
    goal = msg

rospy.init_node("turtle3_node", anonymous=True)
rospy.wait_for_service("spawn")
spawner = rospy.ServiceProxy("spawn", turtlesim.srv.Spawn)
spawner(6.5,6.5,0,"turtle3")
pub = rospy.Publisher("/turtle3/cmd_vel", Twist , queue_size=10)
pose_sub = rospy.Subscriber("pose", Pose, posecallback3)
goal_sub = rospy.Subscriber("goal", Pose, goalcallback3)
pose = Pose()
goal = Pose()
vel = Twist()
rate = rospy.Rate(30)

# k_linear and k_angular are taken as 1.5 and 6 respectively
distance = math.sqrt((goal.x - pose.x + 2) ** 2 + (goal.y - pose.y + 2) ** 2)
angle = math.atan2(goal.y - pose.y + 2, goal.x - pose.x + 2)
vel.linear.x = 0
vel.angular.z = 0
pub.publish(vel)
while not rospy.is_shutdown():
    while distance > 0.1:
        distance = math.sqrt((goal.x - pose.x + 2) ** 2 + (goal.y - pose.y + 2) ** 2) #linear error
        angle = math.atan2(goal.y - pose.y + 2, goal.x - pose.x + 2) #angular error
        lin_vel = 1.5 * distance
        ang_vel = 6 * (angle - pose.theta)
        vel.linear.x = lin_vel
        vel.angular.z = ang_vel
        pub.publish(vel)
        rate.sleep()
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    distance = math.sqrt((goal.x - pose.x + 2) ** 2 + (goal.y - pose.y + 2) ** 2)
    angle = math.atan2(goal.y - pose.y + 2, goal.x - pose.x + 2)
rospy.spin()