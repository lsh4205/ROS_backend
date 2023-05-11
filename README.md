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

  
## Reference
- [ROS - *Publisher* and *Subscriber*](https://medium.com/swlh/part-3-create-your-first-ros-publisher-and-subscriber-nodes-2e833dea7598#:~:text=A%20ROS%20Node%20can%20be,is%20published%20to%20the%20Topic)
- [ROS Docker Tutorial](http://wiki.ros.org/docker/Tutorials/Docker)
- [rosbag Cookbook](http://wiki.ros.org/rosbag/Cookbook) & [rosbag Python API](https://wiki.ros.org/rosbag/Code%20API#py_api)
- Data
  - `geometry_msgs/Twist` - [link](http://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html)
  - `sensor_msgs/PointCloud2` - [link](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html)
- [ros_numpy](http://docs.ros.org/en/noetic/api/ros_numpy/html/namespaceros__numpy.html)
- [ros_numpy.point_cloud2](http://docs.ros.org/en/noetic/api/ros_numpy/html/namespaceros__numpy_1_1point__cloud2.html#a6c94da026739ddec4e093ef792bdcc9a)
