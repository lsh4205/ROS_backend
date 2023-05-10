import os
import rospy
import rosbag
import pcl

ANOMALY_VELOCITY_THRESHOLD = 4.5
DELTA_T = 2.0
SITE_NAME = "BMW"
BAG_FILE = "data.bag"