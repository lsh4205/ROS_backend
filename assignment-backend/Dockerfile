FROM ros:noetic

RUN apt-get update && \
    apt-get install -y \
        python3-pip \
        ros-noetic-ros-numpy \ 
        python3-pcl && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && \
    pip3 install pycryptodomex python-gnupg numpy

RUN mkdir /workspace
WORKDIR /workspace

COPY anomaly_detector.py /workspace/anomaly_detector.py
COPY data.bag /workspace/data.bag