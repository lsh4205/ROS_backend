# Real-Time ROS 
### Process
1. Run `roscore`. `roscore` is a collection of nodes and programs that are pre-requisites of a ROS-based system. You must have a `roscore` running in order for ROS nodes to communicate.

    `docker run --net=host --rm -it rt-anomaly-detector roscore`

2. Play `data.bag` file to simulate real-time data in our system.

    `docker run --net=host -it rt-anomaly-detector rosbag play data.bag`