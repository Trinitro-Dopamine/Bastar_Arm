#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
import cv2 as cv
from cv_bridge import CvBridge
import numpy as np
from std_msgs.msg import Float32MultiArray

def near(img):
    copyimg = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    _, mask = cv.threshold(copyimg, 125, 255, cv.THRESH_BINARY)
    element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    dst = cv.morphologyEx(mask, cv.MORPH_OPEN, element)
    dst = cv.morphologyEx(dst, cv.MORPH_CLOSE, element)
    dst_copy = dst.copy()
    img3,contours3,hierarchy3 = cv.findContours(dst_copy,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    lenght = []
    x_center,y_center = 0,0
    for i in range(len(contours3)):
        # draw0 = np.zeros([dst.shape[0], dst.shape[1]], dtype=np.uint8)
        rect = cv.minAreaRect(contours3[i])
        box = cv.boxPoints(rect)
        x = box[0]
        y = box[1]
        z = box[2]
        w = box[3]
        x_center = int(x[0] / 4 + y[0] / 4 + z[0] / 4 + w[0] / 4)
        y_center = int(x[1] / 4 + y[1] / 4 + z[1] / 4 + w[1] / 4)
        l = np.sqrt(np.power(x_center-380,2)+np.power(y_center-160,2))
        lenght.append(l)
    arg = np.argmin(lenght)
    rect = cv.minAreaRect(contours3[arg])
    box = cv.boxPoints(rect)
    x = box[0]
    y = box[1]
    z = box[2]
    w = box[3]
    x_center = int(x[0] / 4 + y[0] / 4 + z[0] / 4 + w[0] / 4)
    y_center = int(x[1] / 4 + y[1] / 4 + z[1] / 4 + w[1] / 4)
    draw0 = np.zeros([dst.shape[0], dst.shape[1]], dtype=np.uint8)
    cv.drawContours(draw0, contours3, arg, 255, -1)
    return x_center,y_center,draw0


def callback0(imgmsg):
    pub_p = rospy.Publisher('left_hand_camera', Float32MultiArray, queue_size=10)
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg)
    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]
    img = cv.merge([b,g,r])
    image = img.copy()
    x_center, y_center, draw = near(image)
    #theta = get_theta(draw)
    #if theta > 90:
    #    theta = theta - 180
    # img = fill_color(img,320,200)
    # element = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    # dst = cv.morphologyEx(img, cv.MORPH_OPEN, element)
    # dst = cv.morphologyEx(dst, cv.MORPH_CLOSE, element)
    # index = np.where(dst == 255)
    # size = index[0].size
    # dst_copy = dst.copy()
    # x_center,y_center,theta= 0 ,0 ,0
    # if size<15000 and size>0:
    #     theta = get_theta(dst_copy)
    #     if theta > 90:
    #         theta = theta - 180
    #     img3,contours3,hierarchy3 = cv.findContours(dst_copy,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #     rect = cv.minAreaRect(contours3[0])
    #     box = cv.boxPoints(rect)
    #     x = box[0]
    #     y = box[1]
    #     z = box[2]
    #     w = box[3]
    #     x_center = int(x[0] / 4 + y[0] / 4 + z[0] / 4 + w[0] / 4)
    #     y_center = int(x[1] / 4 + y[1] / 4 + z[1] / 4 + w[1] / 4)
    #     # print(x_center,y_center,theta)
    cv.circle(img, (x_center,y_center), 5, (0, 0, 255))
    cv.circle(img, (352,173),5 , (255, 0, 0))
    #right_hand = Float32MultiArray(data = [x_center-352,y_center-173,theta] )
    # rospy.loginfo(right_hand)
    #pub_p.publish(right_hand)
    #combine=np.hstack([img,draw])
    cv.imshow("left", draw)
    cv.waitKey(10)



def listener():
    rospy.init_node('left_hand_image', anonymous=True)

    rospy.Subscriber("/cameras/left_hand_camera/image", Image, callback0)
    rospy.spin()



if __name__ == '__main__':
     listener()
