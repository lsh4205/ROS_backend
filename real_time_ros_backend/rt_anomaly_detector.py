import os
import rospy
import rosbag
import pcl
import ros_numpy
import numpy as np
from collections import deque

from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2

ANOMALY_VELOCITY_THRESHOLD = 4.5
DELTA_T = 2.0
SITE_NAME = "BMW"
# BUFFER SIZE can be changed depend on the average data per second.
# It can be calculated based on the previous record
# BUFFER_SIZE can be max(num_velocity, num_PC2) * 1.2 
BUFFER_SIZE = 200

class AnomalyDetector:
    def __init__(self):
        self.anomalies =[]
        self.point_clouds = deque(maxlen=BUFFER_SIZE)
        rospy.init_node("velocity_anomaly_detector")

        self.velocity_sub = rospy.Subscriber("/velocity", Twist, self.velocity_callback)


    def velocity_callback(self, msg):
        if msg.linear.z > ANOMALY_VELOCITY_THRESHOLD:
            pass

    def points_clouds_collect(self, incident_time):
        # Collect pointclouds between 2 seconds before anomaly 
        # and 2 seconds after the anomaly in `.pcd`.
        start_time = incident_time - DELTA_T
        end_time = incident_time + DELTA_T

        # Select point clouds that are in range.
        point_clouds = [pc for pc in self.point_clouds if start_time <= pc[0] <= end_time]

        # Store all collected `pcd`s as `{SITE_NAME}/{INCIDENT_TIME}/{FRAME_TIME}.pcd`.
        # 1. Create {SITE_NAME}/{INCIDENT_TIME} directory.
        incident_dir = os.path.join(SITE_NAME, str(incident_time))
        os.makedirs(incident_dir, exist_ok=True)

        for t, pc in point_clouds:
            # 2. Create {FRAME_TIME}.pcd file from point cloud.
            pcd_name = str(t) + '.pcd'
            file_path = os.path.join(incident_dir, pcd_name)

            # In Python, there is no direct way to convert point cloud to '.pcd' file.
            # Therefore, convert point cloud to xyz_array with ros_numpy function called 'pointcloud2_to_xyz_array'.
            pc_array = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(pc)
            
            cloud = pcl.PointCloud()
            cloud.from_array(pc_array.astype(np.float32))
            pcl.save(cloud, file_path, format="pcd")

def main():

    anomaly_detector = AnomalyDetector()
    print(anomaly_detector.anomalies)

main()