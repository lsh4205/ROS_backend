# ROS_backend
This document provides the necessary steps for setting up the `ros-anomaly-detector` Docker image and details regarding the Python script responsible for detecting and collecting abnormal data, which is designed for the Robot Operating System(ROS).

## Prerequisites
1. Create a Dockerfile
 - The Dockerfile contains all the commandlines to assemble an image to ensure all the dependencies, libraries, and tools needed for the application to run.
2. Update `apt-get` with `apt-get update`.
 - Update Advanced Packaging Tool(APT) to ensure the latest versions are installed.
3. Install all necessary modules with `apt-get install -y`
  - `ros-noetic-ros-numpy`
    - Install `ros_numpy` to convert PointCloud2 message to array format.
  - `python3-pcl`
    - Create a PCL point cloud and populates it with the data from the numpy array.
  - `python3-pip`
    - `rosbag` Python package uses `Cryptodomex` and `gnupg` pagckages based on [rosbag/Cookbook](http://wiki.ros.org/rosbag/Cookbook).
    
      `$ pip3 install pycryptodomex python-gnupg`
    
4. Build Docker image called **ros-anomaly-detector** using the following command:

    `$ docker build -t ros-anomaly-detector .`
  
5. Run Docker and test with Rosbag
 - Upon completing the setup procedures, `rosbag info data.bag` command will provide a summary of the contents stored in the bag file.
  
    `$ docker run --rm ros-anomaly-detector rosbag info data.bag`
  
6. Run **ros-anomaly-detector** image.

    `$ docker run --rm -v $(pwd):/workspace ros-anomaly-detector python3 /workspace/anomaly-detector.py`
    
## Code Implementation and Configuration
#### 1) Initial SetUp
```python
# Import all the necessary modules
import os
import rosbag
import pcl
import ros_numpy
import numpy as np

# Constants 
ANOMALY_VELOCITY_THRESHOLD = 4.5
DELTA_T = 2.0
SITE_NAME = "BMW"
BAG_FILE = "data.bag"
```
#### 2) Declare Class
```python
class AnomalyDetector:
    # anomalies: Collect all the abnormal incident times.
    # point_clouds: Collect all the PointCloud2 with time.
    def __init__(self):
        self.anomalies =[]
        self.point_clouds = []
```
#### 3) Process data.bag file
```python
# Process bag file with rosbag
def process_rosbag_file(self):
        bag = rosbag.Bag(BAG_FILE, "r")
        # Read messages from data.bag
        for topic, msg, t in bag.read_messages():
            # If topic is '/velocity', call celocity_callback()
            if topic == "/velocity":
                self.velocity_callback(msg, t.to_sec())
            # If topic is '/lidar_0000/os_cloud_node/points',
            # append it to 'point_clouds'
            elif topic == "/lidar_0000/os_cloud_node/points":
                self.point_clouds.append((t.to_sec(), msg))
```
#### 4) Detect anomalies
Based on the definition of anomaly from description, if $z$ component of velocity is larger than $4.5$ at any given frame, that frame is defined as abnormal frame.
```python
# msg: velocity message
# t: incident time
def velocity_callback(self, msg, t):
    # Detect anomaly 
    # if z-compnent of velocity is over ANOMALY_VELOCITY_THRESHOLD
    if msg.linear.z > ANOMALY_VELOCITY_THRESHOLD:
        incident_time = t
        # Append incident_time to self.anomalies
        self.anomalies.append(incident_time) 
        # Callback points_cloud_collect to collect point clouds in range
        self.points_clouds_collect(incident_time)
```
#### 5) Collect point clouds in range
```python
def points_clouds_collect(self, incident_time):
    # Collect pointclouds between 2 seconds before anomaly 
    # and 2 seconds after the anomaly in `.pcd`.
    start_time = incident_time - DELTA_T
    end_time = incident_time + DELTA_T
```
```python
# Select point clouds that are in range.
point_clouds = [pc for pc in self.point_clouds if start_time <= pc[0] <= end_time]
```
```python
# Store all collected `pcd`s as `{SITE_NAME}/{INCIDENT_TIME}/{FRAME_TIME}.pcd`.
# 1. Create {SITE_NAME}/{INCIDENT_TIME} directory.
incident_dir = os.path.join(SITE_NAME, str(incident_time))
os.makedirs(incident_dir, exist_ok=True)
```
```python
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
```
## Reference
- [ROS - *Publisher* and *Subscriber*](https://medium.com/swlh/part-3-create-your-first-ros-publisher-and-subscriber-nodes-2e833dea7598#:~:text=A%20ROS%20Node%20can%20be,is%20published%20to%20the%20Topic)
- [ROS Docker Tutorial](http://wiki.ros.org/docker/Tutorials/Docker)
- [rosbag Cookbook](http://wiki.ros.org/rosbag/Cookbook) & [rosbag Python API](https://wiki.ros.org/rosbag/Code%20API#py_api)
- Data
  - `geometry_msgs/Twist` - [link](http://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html)
  - `sensor_msgs/PointCloud2` - [link](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html)
- [ros_numpy](http://docs.ros.org/en/noetic/api/ros_numpy/html/namespaceros__numpy.html)
- [ros_numpy.point_cloud2](http://docs.ros.org/en/noetic/api/ros_numpy/html/namespaceros__numpy_1_1point__cloud2.html#a6c94da026739ddec4e093ef792bdcc9a)
