#!/bin/sh

set +e
# As an improvement, git clone always on startup
# Or run a 15 min crontab thatcheck for new updates to github, then pull 
# the source code, and then rebuild and startup docker container.

cd /home/piapp/alligator-swarm-copter
docker-compose up -d telemetary
