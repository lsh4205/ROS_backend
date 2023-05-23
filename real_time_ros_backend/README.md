# Real-Time ROS 
### Process
1. Run `roscore`. `roscore` is a collection of nodes and programs that are pre-requisites of a ROS-based system. You must have a `roscore` running in order for ROS nodes to communicate.

    `docker run --net=host --rm -it rt-anomaly-detector roscore`

2. Play `data.bag` file to simulate real-time data in our system.

    `docker run --net=host -it rt-anomaly-detector rosbag play data.bag`

3. Record the selective real-time topic from robot into `.bag` file. [Reference](https://www.youtube.com/watch?v=Vlp0e89TXpI)

    `rosbag record /velocity /lidar_0000/os_cloud_node/points {/and_so_on}`
