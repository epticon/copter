# Alligator Copter Telemetary

Responsible for transmitting information back and forth from the copter to the server, and vcise versa.

## Todo

- [ ] Replace existing base container image with `alpine-python:slim`.
- [ ] Switch application `python 3` once `pymavlink` and `ardupilot` have integrated suppot for python 3 into their individual library.
- [ ] Remove `vim`, `python3.6-venv`.
- [ ] Lock down the ubuntu version foe telemetary to specific version, maybe `16.*`
- [ ] Optimize the current **telemetary** `Dockerfile` with [OptimizedDockerFile](./stub/OptimizedDockerFile).
