#!/usr/bin/env python 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import std_msgs.msg
import sensor_msgs.msg
from std_msgs.msg import Header
import geometry_msgs.msg
import math

def circle(radius,res,start):
   waypoints = []
   waypoints.append(start)

   for i in range(0,res):
      point = copy.deepcopy(start)
      point.position.x += radius*math.cos((2*math.pi/res)*i)
      point.position.y += radius*math.sin((2*math.pi/res)*i)
      point.position.z =.2

      print i, point.position.x, point.position.y

      waypoints.append(copy.deepcopy(point))
   waypoints.append(start)
   return waypoints                

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_circle', anonymous=True)  #initialize moveit_commander

robot = moveit_commander.RobotCommander()    #robot commander to interface to the robot
scene = moveit_commander.PlanningSceneInterface()
arm_group = moveit_commander.MoveGroupCommander('arm')      #moving group commander

## creating a display trajextory publisher which is used later to publish trajectories fro Rviz to visualize
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

r = .075

path_points = circle(r, 100, arm_group.get_current_pose().pose)


(plan, fraction) = arm_group.compute_cartesian_path(
                                   path_points,   # waypoints to follow
                                   0.01,        # eef_step
                                   0.0)         # jump_threshold

plan = arm_group.retime_trajectory(robot.get_current_state(), plan, .05)  # (0.02) time scaling factor


display_trajectory = moveit_msgs.msg.DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan)
# Publish
display_trajectory_publisher.publish(display_trajectory);

arm_group.execute(plan, wait=True)
# Excutes trajectory

moveit_commander.roscpp_shutdown()