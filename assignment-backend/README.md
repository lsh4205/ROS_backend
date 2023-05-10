# Assignment-anomaly-detection
## Overview
- an edge device is deployed in `BMW` factory in germany.
- one day, an engineer found out that there is a bug in our software.
- his guess is that system fails when z component of velocity is faster than `4.5`
- he wants to reproduce bug in lab and asks you to write program to collect abnormal data.

## Specifications
### Input Data
- you are given single rosbag file `data.bag` collected from the site.
- site environment can be simulated by playing given rosbag file.

```bash
$ rosbag info data/data.bag
path:         data/data.bag
version:      2.0
duration:     1:21s (81s)
start:        Dec 22 2021 01:29:01.30 (1640136541.30)
end:          Dec 22 2021 01:30:22.50 (1640136622.50)
size:         658.9 MB
messages:     12991
compression:  lz4 [812/812 chunks; 54.07%]
uncompressed:   1.2 GB @ 15.0 MB/s
compressed:   658.5 MB @  8.1 MB/s (54.07%)
types:        geometry_msgs/Twist     [9f195f881246fdfa2798d1d3eebca84a]
              sensor_msgs/PointCloud2 [1158d486dd51d683ce2f1be655c3c181]
topics:       /lidar_0000/os_cloud_node/points     811 msgs    : sensor_msgs/PointCloud2
              /velocity                          12180 msgs    : geometry_msgs/Twist
```
- as attached screen above
  * pointcloud : `/lidar_0000/os_cloud_node/points`
  * velocity : `/velocity`
- for more information regarding playing rosbag file refer [link](http://wiki.ros.org/rosbag/Commandline)

### Definition of Anomaly
- if z component of velocity is larger than `4.5` at any given frame, that frame is abnormal frame

### Data to Collect
- collect pointclouds between 2 seconds before anomaly and 2 seconds after the anomaly in `.pcd`

### Output format
- store all collected `pcd`s as `{SITE_NAME}/{INCIDENT_TIME}/{FRAME_TIME}.pcd`
- all times are in UNIX time including nanoseconds from ros.

### Software
- any language or package is allowed.

## Things to submit
1. create git repository in github and invite interviewers listed in the email
2. commit your progress from time to time.
3. if you have any questions utilise issue tab and **tag** interviewers.
4. when you are finished. please write a single document explaining
  * how you designed your code and system.
  * what can be further improved.
5. create single `zip` file containing `1-2` and send it.

## Tips
1. this can be done multiple ways the easiest way will be to design appropriate callback function for each topic and add them.
2. you may add some assumptions for things not specified in this document.
3. don't be late
