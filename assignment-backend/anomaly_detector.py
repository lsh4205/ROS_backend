import os
import rospy
import rosbag
import pcl

ANOMALY_VELOCITY_THRESHOLD = 4.5
DELTA_T = 2.0
SITE_NAME = "BMW"
BAG_FILE = "data.bag"

class AnomalyDetector:
    def __init__(self):
        self.anomalies =[]
        self.point_clouds = []

    def process_rosbag_file(self):
        bag = rosbag.Bag(BAG_FILE, "r")
        te = True
        for topic, msg, t in bag.read_messages():
            if topic == "/velocity":
                self.velocity_callback(msg, t.to_sec())
            elif topic == "/lidar_0000/os_cloud_node/points":
                self.point_clouds.append((t.to_sec(), msg))