import os
import rosbag
import pcl
import ros_numpy
import numpy as np

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
        for topic, msg, t in bag.read_messages():
            if topic == "/velocity":
                self.velocity_callback(msg, t.to_sec())
                
            elif topic == "/lidar_0000/os_cloud_node/points":
                self.point_clouds.append((t.to_sec(), msg))

    def velocity_callback(self, msg, t):
        if msg.linear.z > ANOMALY_VELOCITY_THRESHOLD:
            incident_time = t
            self.anomalies.append(incident_time) 
            self.points_clouds_collect(incident_time)

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
    anomaly_detector.process_rosbag_file()
    print(anomaly_detector.anomalies)

main()