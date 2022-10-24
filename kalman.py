#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import numpy

#Variables and Initiation
Zn = 0                                                              #Measurement Value from Sensor
Rn = 0.01                                                           #Measurement Uncertainty - Should be given in datasheet for the sensor
q = 0.001                                                           #Process Noise
sys_state, sys_uncertainty = 0, 0                                   #Xn and Pn
prev_state, prev_uncertainty = 0, 100                               #Xn-Hat and Pn-Hat
# predicted_state, predicted_uncertainty = 0,0                      #Xn+1-Hat and Pn+1-Hat. useless for now but can be used if we switch from constant to Dynamic Model
Kn = (prev_uncertainty)/(prev_uncertainty+Rn)                       #Kalman Gain

#Initial State Prediction

#Setup ROS Subscriber and Publisher Node
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    Zn = data.data                                                  #Get Measurements

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("Yaw", Float32, callback)
    rospy.spin()

def talker():
    pub = rospy.Publisher('KalmanYaw', Float32)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        kalmanYaw = sys_state
        rospy.loginfo(kalmanYaw)
        pub.publish(kalmanYaw)
        rate.sleep()


if __name__ == '__main__':
    listener()

    #State Update
    Kn = (prev_uncertainty)/(prev_uncertainty+Rn)
    sys_uncertainty = (1 - Kn)*prev_state + q
    sys_state = (1-Kn)*prev_state + Kn*Zn

    #State Predict - assuming a constant model
    prev_state = sys_state
    prev_uncertainty = sys_uncertainty

    try:
        talker()
    except rospy.ROSInterruptException:
        pass
