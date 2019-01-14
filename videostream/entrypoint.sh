#!/bin/bash

ffmpeg -re -f video4linux2 -i /dev/video0 -c:v libx264 -profile:v baseline -c:a aac -f flv -pix_fmt yuv420p $STREAMING_SERVER_URL