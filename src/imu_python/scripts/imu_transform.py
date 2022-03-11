#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Quaternion
import copy
import tf
import math
y=1
z=1

def callback(msg):
    global y
    global z
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
    msg=str(msg)
    ax=0
    ay=0
    az=0
    gx=0
    gy=0
    gz=0
    num=0
    s=""
    for i in range(7,len(msg)):
        if msg[i]=='/' and num==0:
            num=num+1
            ax=int(s)
            s=""

        elif msg[i]=='/' and num==1:
            num=num+1
            ay=int(s)
            s=""

        elif msg[i]=='/' and num==2:
            num=num+1
            az=int(s)
            s=""
        elif msg[i]=='/' and num==3:
            num=num+1
            gx=int(s)
            s=""

        elif msg[i]=='/' and num==4:
            num=num+1
            gy=int(s)
            s=""

        elif msg[i]=='/' and num==5:
            num=num+1
            gz=int(s)
            s=""
        
        else:
            s=s+msg[i]
    pitch = math.atan(ax/math.sqrt((ay*ay) + (az*az)))
    roll = math.atan(ay/math.sqrt((ax*ax) + (az*az)))
    yaw = math.atan(az/math.sqrt((ax*ax) + (ay*ay)))
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    q= Quaternion()
    q.x=qx
    q.y=qy
    q.z=qz
    q.w=qw
    pub = rospy.Publisher('chatter', Quaternion, queue_size=20)
    pub.publish(q)
    '''print(qx)
    print(qy)
    print(qz)
    print(qw)'''

    
    
rospy.init_node('listener', anonymous=True)
sub = rospy.Subscriber('/imu', String ,callback) 



rospy.spin()