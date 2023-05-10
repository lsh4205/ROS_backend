# ROS_backend
## Docker Setting
1. Update `apt-get` with `apt-get update`.
2. Install all necessary modules with `apt-get install -y`
  a. `python3-pip`
    - rosbag Python package uses `Cryptodomex` and `gnupg` pagckages based on [rosbag/Cookbook](http://wiki.ros.org/rosbag/Cookbook). They can be installed via `pip` using: 
    
      `$ pip3 install pycryptodomex python-gnupg`
    
3. Build Docker image called **ros-anomaly-detector** with following commandline.

    `$ docker build -t ros-anomaly-detector .`
  
4. Run Docker and test with `rosbag info data.bag`.S ite environment can be simulated by playing given rosbag file.
  
    `$ docker run --rm ros-anomaly-detector rosbag info data.bag`
  
5. Run **ros-anomaly-detector** image.
  `$ docker run --rm -v $(pwd):/workspace ros-anomaly-detector python3 /workspace/anomaly-detector.py`
## Reference
- [ROS - *Publisher* and *Subscriber*](https://medium.com/swlh/part-3-create-your-first-ros-publisher-and-subscriber-nodes-2e833dea7598#:~:text=A%20ROS%20Node%20can%20be,is%20published%20to%20the%20Topic)
- [ROS Docker Tutorial](http://wiki.ros.org/docker/Tutorials/Docker)
- [rosbag Cookbook](http://wiki.ros.org/rosbag/Cookbook) & [rosbag Python API](https://wiki.ros.org/rosbag/Code%20API#py_api)
- Data
  - `geometry_msgs/Twist` - [link](http://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html)
  - `sensor_msgs/PointCloud2` - [link](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html)
- [pypcd](https://github.com/dimatura/pypcd)
