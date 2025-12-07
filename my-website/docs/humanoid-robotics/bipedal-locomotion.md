---
sidebar_position: 1
---

# Bipedal Locomotion

Teaching a humanoid robot to walk is one of the most challenging and rewarding tasks in robotics. This chapter explores the fundamentals of bipedal locomotion.

## The Challenge of Walking

Unlike wheeled robots, bipedal robots must:

- **Maintain Balance** while supported by only one or two feet
- **Generate Locomotion** through coordinated leg movements
- **Handle Disturbances** and recover from perturbations
- **Optimize Energy** to walk efficiently

## Humanoid Robot Models

Let's work with a simple humanoid in PyBullet:

```python
import pybullet as p
import pybullet_data
import numpy as np
import time

# Setup simulation
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.setTimeStep(1./240.)

# Load environment
plane = p.loadURDF("plane.urdf")

# Load humanoid robot
humanoid = p.loadURDF("humanoid/humanoid.urdf", [0, 0, 0.9])

# Get joint information
num_joints = p.getNumJoints(humanoid)
print(f"Humanoid has {num_joints} joints")

for i in range(num_joints):
    joint_info = p.getJointInfo(humanoid, i)
    print(f"Joint {i}: {joint_info[1].decode('utf-8')}, Type: {joint_info[2]}")
```

## Center of Mass and Stability

The key to walking is keeping the Center of Mass (CoM) over the support polygon:

```python
def get_center_of_mass(robot_id):
    """Calculate robot's center of mass"""
    total_mass = 0
    com_position = np.zeros(3)
    
    # Base link
    base_pos, _ = p.getBasePositionAndOrientation(robot_id)
    base_mass = p.getDynamicsInfo(robot_id, -1)[0]
    com_position += np.array(base_pos) * base_mass
    total_mass += base_mass
    
    # All other links
    num_joints = p.getNumJoints(robot_id)
    for i in range(num_joints):
        link_state = p.getLinkState(robot_id, i)
        link_pos = np.array(link_state[0])
        link_mass = p.getDynamicsInfo(robot_id, i)[0]
        
        com_position += link_pos * link_mass
        total_mass += link_mass
    
    com_position /= total_mass
    return com_position

def is_stable(robot_id, support_foot_links):
    """Check if CoM is over support polygon"""
    com = get_center_of_mass(robot_id)
    
    # Get support foot positions
    foot_positions = []
    for link_id in support_foot_links:
        link_state = p.getLinkState(robot_id, link_id)
        foot_positions.append(link_state[0][:2])  # Only x, y
    
    # Simple check: CoM x,y within convex hull of foot positions
    # (Simplified - in practice use proper convex hull algorithm)
    foot_positions = np.array(foot_positions)
    com_xy = com[:2]
    
    return True  # Placeholder for proper stability check
```

## Zero Moment Point (ZMP)

The ZMP is a crucial concept for bipedal walking:

```python
def calculate_zmp(robot_id):
    """
    Calculate Zero Moment Point
    ZMP is the point on the ground where total inertial and gravitational
    forces have zero moment
    """
    # Get CoM and its derivatives
    com = get_center_of_mass(robot_id)
    # In practice, you'd calculate CoM velocity and acceleration
    com_vel = np.zeros(3)  # Placeholder
    com_acc = np.array([0, 0, -9.81])  # Gravity
    
    # ZMP calculation (simplified)
    # zmp_x = com_x - (com_z / com_acc_z) * com_acc_x
    # zmp_y = com_y - (com_z / com_acc_z) * com_acc_y
    
    if com_acc[2] != 0:
        zmp_x = com[0] - (com[2] / com_acc[2]) * com_acc[0]
        zmp_y = com[1] - (com[2] / com_acc[2]) * com_acc[1]
    else:
        zmp_x, zmp_y = com[0], com[1]
    
    return np.array([zmp_x, zmp_y, 0])
```

## Simple Walking Controller

Let's implement a basic walking gait:

```python
class SimpleWalkingController:
    def __init__(self, robot_id):
        self.robot = robot_id
        self.phase = 0  # Walking phase
        self.step_duration = 1.0  # seconds per step
        self.step_height = 0.05  # meters
        
        # Joint indices (example - adjust for your robot)
        self.left_hip = 2
        self.left_knee = 3
        self.left_ankle = 4
        self.right_hip = 5
        self.right_knee = 6
        self.right_ankle = 7
    
    def get_joint_targets(self, t):
        """Calculate target joint angles based on walking phase"""
        # Sinusoidal gait pattern
        phase = (t % self.step_duration) / self.step_duration
        angle = 2 * np.pi * phase
        
        # Hip swing
        hip_angle = 0.3 * np.sin(angle)
        
        # Knee bend
        knee_angle = 0.5 * max(0, np.sin(angle))
        
        if phase < 0.5:  # Left leg swing
            targets = {
                self.left_hip: hip_angle,
                self.left_knee: knee_angle,
                self.left_ankle: -0.1,
                self.right_hip: -hip_angle * 0.5,
                self.right_knee: 0,
                self.right_ankle: -0.1,
            }
        else:  # Right leg swing
            targets = {
                self.left_hip: -hip_angle * 0.5,
                self.left_knee: 0,
                self.left_ankle: -0.1,
                self.right_hip: hip_angle,
                self.right_knee: knee_angle,
                self.right_ankle: -0.1,
            }
        
        return targets
    
    def step(self, t):
        """Execute one control step"""
        targets = self.get_joint_targets(t)
        
        for joint_id, target_angle in targets.items():
            p.setJointMotorControl2(
                self.robot,
                joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=target_angle,
                force=500,
                maxVelocity=2.0
            )

# Usage
controller = SimpleWalkingController(humanoid)

for i in range(5000):
    t = i / 240.0  # Time in seconds
    controller.step(t)
    p.stepSimulation()
    time.sleep(1./240.)
```

## Reinforcement Learning for Walking

Train a robot to walk using PPO:

```python
import gym
from stable_baselines3 import PPO

class HumanoidWalkEnv(gym.Env):
    """Gym environment for humanoid walking"""
    
    def __init__(self):
        super().__init__()
        
        # Setup PyBullet
        self.physics_client = p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81)
        
        # Load robot
        self.humanoid = p.loadURDF("humanoid/humanoid.urdf", [0, 0, 0.9])
        
        # Define spaces
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(8,), dtype=np.float32
        )
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(44,), dtype=np.float32
        )
    
    def reset(self):
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        self.humanoid = p.loadURDF("humanoid/humanoid.urdf", [0, 0, 0.9])
        return self._get_obs()
    
    def _get_obs(self):
        # Get base position and orientation
        base_pos, base_orn = p.getBasePositionAndOrientation(self.humanoid)
        base_vel, base_ang_vel = p.getBaseVelocity(self.humanoid)
        
        # Get joint states
        joint_states = p.getJointStates(self.humanoid, range(8))
        joint_pos = [state[0] for state in joint_states]
        joint_vel = [state[1] for state in joint_states]
        
        # Combine all observations
        obs = np.concatenate([
            base_pos, base_orn, base_vel, base_ang_vel,
            joint_pos, joint_vel
        ])
        return obs.astype(np.float32)
    
    def step(self, action):
        # Apply actions to joints
        for i, a in enumerate(action):
            p.setJointMotorControl2(
                self.humanoid, i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=a,
                force=500
            )
        
        p.stepSimulation()
        
        # Get new state
        obs = self._get_obs()
        
        # Calculate reward
        base_pos, _ = p.getBasePositionAndOrientation(self.humanoid)
        
        # Reward forward movement
        forward_reward = base_pos[0]
        
        # Penalty for falling
        height = base_pos[2]
        alive_bonus = 1.0 if height > 0.5 else 0
        
        # Energy penalty
        energy_penalty = -0.01 * np.sum(np.square(action))
        
        reward = forward_reward + alive_bonus + energy_penalty
        done = height < 0.5
        
        return obs, reward, done, {}

# Train the agent
env = HumanoidWalkEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000000)
model.save("humanoid_walk")
```

## Key Concepts

- **Static Stability** – CoM always over support polygon (slow but stable)
- **Dynamic Stability** – ZMP-based control (allows faster walking)
- **Gait Patterns** – Coordinated sequences of leg movements
- **Balance Recovery** – Responding to external disturbances

## Practice Exercises

:::tip Exercise 1: Analyze Stability

Implement a real-time visualization of the CoM and support polygon during walking.

:::

:::tip Exercise 2: Improve Gait

Modify the walking controller to include ankle and hip strategies for better balance.

:::

:::tip Exercise 3: RL Experiment

Train a humanoid to walk backwards or sideways using reinforcement learning.

:::

## Next Steps

Ready to add intelligence? Learn about [computer vision for robotics](/docs/perception/computer-vision) to give your robot eyes!
