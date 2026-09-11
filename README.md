# Intercropping Robot

Software stack for a mobile robot developed for agricultural intercropping research.

This repository contains the ROS 2 packages used to model, simulate, and control a mobile robotic platform for autonomous intercropping applications. The project serves as a development platform for researching and evaluating robot navigation, perception, control, and implement integration in agricultural environments.

---

## Requirements

* Ubuntu 24.04 LTS
* ROS 2 Jazzy
* Gazebo Harmonic
* Python 3

External ROS packages are managed using the provided `.repos` file.

---

## Workspace Setup

Create a ROS 2 workspace:

```bash
mkdir -p ~/<ros_workspace>/src
cd ~/<ros_workspace>/src
```

Clone this repository:

```bash
git clone git@github.com:jepp4561/intercropping_robot.git
```

Import external dependencies:

```bash
cd ..
vcs import src < src/intercropping_robot/intercropping_robot.repos
```

---

## Building

From the workspace root:

```bash
colcon build --symlink-install
```

To rebuild only a specific package:

```bash
colcon build --symlink-install --packages-select <package_name>
```

---

## Running

Launch the simulation:

```bash
ros2 launch robot_bringup sim.launch.py
```
Additionally, display.launch.py can be run to visualize the virtual camera feed:
```bash
ros2 launch robot_description display.launch.py
```
And then adding the camera through the ros topic
Additional launch files are available within the individual packages.

---