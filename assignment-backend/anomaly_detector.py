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
        start_time = incident_time - DELTA_T
        end_time = incident_time + DELTA_T

        point_clouds_in_DELTA_T = [pc for pc in self.point_clouds if start_time <= pc[0] <= end_time]
        incident_dir = os.path.join(SITE_NAME, str(incident_time))
        os.makedirs(incident_dir, exist_ok=True)

        for t, pc in point_clouds:
            pcd_name = t + '.pcd'
            file_path = os.path.join(incident_dir, pcd_name)