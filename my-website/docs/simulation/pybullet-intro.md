---
sidebar_position: 1
---

# Introduction to PyBullet

PyBullet is a Python interface to the Bullet physics engine, perfect for robotics simulation, reinforcement learning research, and testing robot behaviors safely.

## Why PyBullet for Robotics?

- **Realistic Physics** – Accurate collision detection, rigid body dynamics, and contact modeling
- **Fast Simulation** – Efficient C++ backend with Python convenience
- **Rich Features** – Support for URDF/SDF robot models, sensors, actuators
- **Free & Open Source** – MIT licensed, active community support
- **Perfect for RL** – Deterministic simulation ideal for training agents

## Setting Up PyBullet

First, install PyBullet:

```bash
pip install pybullet numpy matplotlib
```

## Your First Robot Simulation

Let's create a simple simulation with a ground plane and a robot:

```python
import pybullet as p
import pybullet_data
import time

# Connect to physics server (GUI mode for visualization)
physics_client = p.connect(p.GUI)

# Set up the simulation environment
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load ground plane
plane_id = p.loadURDF("plane.urdf")

# Load a robot (R2D2 example)
robot_start_pos = [0, 0, 1]
robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF("r2d2.urdf", robot_start_pos, robot_start_orientation)

# Run simulation for 10 seconds
for i in range(10000):
    p.stepSimulation()
    time.sleep(1./240.)  # Real-time playback

p.disconnect()
```

## Understanding URDF Files

URDF (Unified Robot Description Format) defines robot structure:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" 
               iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
  
  <!-- Wheel link -->
  <link name="wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>
  
  <!-- Joint connecting base to wheel -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel"/>
    <origin xyz="0.2 0 -0.1" rpy="1.57 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</robot>
```

## Controlling Robot Joints

PyBullet provides several control modes:

```python
import pybullet as p
import pybullet_data
import numpy as np

# Setup
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
plane = p.loadURDF("plane.urdf")

# Load robot arm (KUKA example)
robot = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)

# Get number of joints
num_joints = p.getNumJoints(robot)
print(f"Robot has {num_joints} joints")

# Position control example
target_positions = [0, 0.5, 0, -1.5, 0, 1.0, 0]  # Target joint angles

for i in range(1000):
    p.setJointMotorControlArray(
        robot,
        jointIndices=range(num_joints),
        controlMode=p.POSITION_CONTROL,
        targetPositions=target_positions
    )
    p.stepSimulation()

# Velocity control example
target_velocities = [1.0] * num_joints

p.setJointMotorControlArray(
    robot,
    jointIndices=range(num_joints),
    controlMode=p.VELOCITY_CONTROL,
    targetVelocities=target_velocities
)

# Torque control (most flexible for RL)
target_torques = [10.0] * num_joints

p.setJointMotorControlArray(
    robot,
    jointIndices=range(num_joints),
    controlMode=p.TORQUE_CONTROL,
    forces=target_torques
)
```

## Creating Custom Environments

Let's build a gym-like environment:

```python
import gym
from gym import spaces
import numpy as np
import pybullet as p

class ReachingEnv(gym.Env):
    """Robot arm reaching task"""
    
    def __init__(self, render=False):
        super().__init__()
        
        # Connect to physics server
        if render:
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Load environment
        self.plane = p.loadURDF("plane.urdf")
        self.robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
        
        # Action space: joint velocities
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(7,), dtype=np.float32
        )
        
        # Observation space: joint positions + target position
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32
        )
        
        self.target_pos = None
    
    def reset(self):
        # Reset robot to initial position
        for i in range(7):
            p.resetJointState(self.robot, i, 0)
        
        # Random target position
        self.target_pos = np.random.uniform([-0.5, -0.5, 0.3], 
                                           [0.5, 0.5, 0.8])
        
        return self._get_obs()
    
    def _get_obs(self):
        # Get joint positions
        joint_states = p.getJointStates(self.robot, range(7))
        joint_pos = [state[0] for state in joint_states]
        
        # Combine with target position
        obs = np.concatenate([joint_pos, self.target_pos])
        return obs.astype(np.float32)
    
    def step(self, action):
        # Apply actions (velocity control)
        for i, vel in enumerate(action):
            p.setJointMotorControl2(
                self.robot, i,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=vel * 2.0
            )
        
        p.stepSimulation()
        
        # Get end effector position
        end_effector_state = p.getLinkState(self.robot, 6)
        end_effector_pos = np.array(end_effector_state[0])
        
        # Calculate reward (negative distance to target)
        distance = np.linalg.norm(end_effector_pos - self.target_pos)
        reward = -distance
        
        # Done if close enough
        done = distance < 0.05
        
        return self._get_obs(), reward, done, {}

# Test the environment
env = ReachingEnv(render=True)
obs = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
```

## Key Concepts

- **Physics Stepping** – Call `p.stepSimulation()` to advance physics
- **Control Modes** – Position, velocity, or torque control for joints
- **State Queries** – Get joint states, link states, contact information
- **URDF Models** – Define robot structure, inertia, and visual appearance

## Practice Exercises

:::tip Exercise 1: Build a Simple Robot

Create a URDF file for a simple 2-wheeled robot and simulate it moving forward.

:::

:::tip Exercise 2: PID Controller

Implement a PID controller to make a robot arm reach a target position smoothly.

:::

:::tip Exercise 3: Collision Detection

Add obstacles to the environment and detect when the robot collides with them.

:::

## Next Steps

Now that you can simulate robots, let's explore [humanoid robot control](/docs/humanoid-robotics/bipedal-locomotion) and make them walk!
