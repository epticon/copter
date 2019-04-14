#!/bin/bash
cd /app && python3 src/main.py &
cd /ardupilot/ArduCopter && sim_vehicle.py
