#ifndef DEBUG_POSITION_CONTROL_H
#define DEBUG_POSITION_CONTROL_H

#include <ros/ros.h>

#include "message_header.h"

#include <sensor_msgs/JointState.h>

#include <dynamixel_workbench_toolbox/dynamixel_workbench.h>
#include <dynamixel_workbench_msgs/DynamixelStateList.h>
#include <dynamixel_workbench_msgs/JointCommand.h>

class DebugPositionControl
{
 private:
  // ROS NodeHandle
  ros::NodeHandle node_handle_;

  // ROS Parameters

  // ROS Topic Publisher
  ros::Publisher dynamixel_state_list_pub_;
  ros::Publisher joint_states_pub_;
  ros::Publisher debug_data_pub_;

  // ROS Topic Subscriber
  ros::Subscriber joint_command_sub_;

  // ROS Service Server
  ros::ServiceServer joint_command_server_;

  // ROS Service Client

  // Dynamixel Workbench Parameters
  DynamixelWorkbench *dxl_wb_;
  uint8_t dxl_id_[16];
  uint8_t dxl_cnt_;

 public:
  DebugPositionControl();
  ~DebugPositionControl();
  void controlLoop(void);

 private:
  void initMsg();

  void initPublisher();
  void initSubscriber();
  
  void dynamixelStatePublish();
  void jointStatePublish();
  
  void debugDataPublish();

  void initServer();
  bool jointCommandMsgCallback(dynamixel_workbench_msgs::JointCommand::Request &req,
                               dynamixel_workbench_msgs::JointCommand::Response &res);
  void goalJointPositionCallback(const sensor_msgs::JointState::ConstPtr &msg);
};

#endif //DEBUG_POSITION_CONTROL_Hs