//
// Created by hit on 2022/2/24.
//

#ifndef WRC_HIT_LIB_REALSENSE_INFO_H
#define WRC_HIT_LIB_REALSENSE_INFO_H

#include <ros/ros.h>
#include <geometry_msgs/PoseArray.h>
#include <std_msgs/Float32MultiArray.h>   // 很重要
#include <std_msgs/Float32.h>

class RealsenseInfo
{
public:
    RealsenseInfo(ros::NodeHandle nh);
    ~RealsenseInfo();
    void blockInfoCallback(const geometry_msgs::PoseArrayConstPtr & camera_msg);
    void leftcameraInfoCallback(const std_msgs::Float32MultiArrayPtr &camera_msg);
    void rightcameraInfoCallback(const std_msgs::Float32MultiArrayPtr &camera_msg);
    std::vector<double> getRightCompensationInfo();
    std::vector<double> getLeftCompensationInfo();
    std::vector<std::vector<double>> getBlockInfo();


private:
    ros::NodeHandle nh;
    ros::Subscriber block_info_sub, lefthand_camera_info_sub,righthand_camera_info_sub;
    bool blockisReceive;
    double blockpos[3][6]; //第一问的积木位置  

};

#endif //WRC_HIT_LIB_REALSENSE_INFO_H