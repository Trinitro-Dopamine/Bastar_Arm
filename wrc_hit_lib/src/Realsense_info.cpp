//
// Created by hit on 2022/2/24.
//

#include <thread>
#include <future>
#include "Realsense_info.h"
#include <std_msgs/Int16.h>   // 很重要
#include <std_msgs/Float32MultiArray.h>   // 很重要

#define L_ARM "left"
#define R_ARM "right"

RealsenseInfo::RealsenseInfo(ros::NodeHandle n)
{
    this->nh=n;
    this->blockisReceive=false;
    block_info_sub=this->nh.subscribe("first_recognition",1000,&RealsenseInfo::blockInfoCallback,this);
    lefthand_camera_info_sub=this->nh.subscribe("left_hand_camera",2,&RealsenseInfo::leftcameraInfoCallback,this);
    righthand_camera_info_sub=this->nh.subscribe("right_hand_camera",2,&RealsenseInfo::rightcameraInfoCallback,this);
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<6;j++)
        {
            blockpos[i][j]=0;
        }
    }
    ros::spinOnce();
}

RealsenseInfo::~RealsenseInfo()
{

}

void RealsenseInfo::blockInfoCallback(const geometry_msgs::PoseArrayConstPtr & camera_msg)
{
    if(camera_msg->poses.size()==0)
    {
        return;
    }
    if(camera_msg->poses[0].position.x>0 &&camera_msg->poses[0].position.x<2)
    {
        this->blockisReceive=true;
        for (int i = 0; i < camera_msg->poses.size(); i++)
        {
            blockpos[i][0] = camera_msg->poses[i].position.x;
            blockpos[i][1] = camera_msg->poses[i].position.y;
            blockpos[i][2] = camera_msg->poses[i].position.z+0.15;
            blockpos[i][3] = 3.14;
            blockpos[i][4] = 0;
            blockpos[i][5] = 3.14;
        }
    }
    else
    {
        ROS_INFO("Camera info isn't valid!");
    }
}

void RealsenseInfo::leftcameraInfoCallback(const std_msgs::Float32MultiArrayPtr &camera_msg)
{

}

void RealsenseInfo::rightcameraInfoCallback(const std_msgs::Float32MultiArrayPtr &camera_msg)
{

}

std::vector<std::vector<double>> RealsenseInfo::getBlockInfo()
{
    while(!blockisReceive)
    {
        ROS_INFO("Wait for block info!");
    }
    std::vector<std::vector<double>> blockpos_temp;
    std::vector<double> help_temp;
    for(int i=0;i<3;i++)
    {
        if(blockpos[i][0]!=0)
        {
            for(int j=0;j<6;j++)
            {
                help_temp.push_back(blockpos[i][j]);
            }
            blockpos_temp.push_back(help_temp);
            help_temp.clear();
        }
    }
    return blockpos_temp;
}

std::vector<double> RealsenseInfo::getLeftCompensationInfo()
{

}

std::vector<double> RealsenseInfo::getRightCompensationInfo()
{

}