# Inverted Pendulum
#### Implementation of control laws on simulated inverted pendulum on ros2

![Output sample](videos/screen-capture.gif)

## To-dos
1) Single Inverted Pendulum
- Crete a new node and add that in the launch file which subscribes to state feedback and publishes to torque input
- [initial state - near upright] Write a controller to balance the inverted pendulum with initial state near upright position and not exactly upright
- [Initial state - downward point at stable equilibrium] Write a controller to first swing up the pendulum, then balance on top.

2) Double Inverted Pendulum
- create a new pacakge with dynamics of an double inverted pendulum

## How-to
1. Clone this repository in /src folder of your ros2 workspace
2. Build and source the workspace. Navigate to your workspace directory and run
```
colcon build --symlink--install
source install/setup.bash
```
3. You can now launch the simulation
4. Create a seperate 'controller' node which uses feedback to determine the torque value to accomplish tasks
```
ros2 launch single_inverted single_inverted_pendulum.launch.py
```

## About 
1. You can change the initial states by varying the values theta0 and theta_dot0
2. custom_msg definitions are used for input and feedback


