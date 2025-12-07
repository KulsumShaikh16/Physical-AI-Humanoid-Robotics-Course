---
sidebar_position: 1
---

# Python Fundamentals

Before diving into Physical AI and robotics, let's ensure you have a solid foundation in Python programming.

## Why Python for Robotics?

Python has become the dominant language in robotics and AI for several reasons:

- **Rich Ecosystem** – Libraries like NumPy, PyTorch, OpenCV, and ROS provide powerful tools
- **Rapid Prototyping** – Quick iteration cycles for testing ideas
- **Community Support** – Extensive documentation and active communities
- **Integration** – Easy to interface with C/C++ for performance-critical code

## Essential Python Concepts

### 1. NumPy for Numerical Computing

NumPy is fundamental for robotics work, handling vectors, matrices, and transformations:

```python
import numpy as np

# Create rotation matrix (45 degrees around Z-axis)
angle = np.pi / 4
rotation_z = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle),  np.cos(angle), 0],
    [0,              0,             1]
])

# Apply rotation to a point
point = np.array([1, 0, 0])
rotated_point = rotation_z @ point
print(f"Rotated point: {rotated_point}")
```

### 2. Object-Oriented Programming

Robotics systems benefit from OOP for modularity and reusability:

```python
class RobotArm:
    def __init__(self, num_joints):
        self.num_joints = num_joints
        self.joint_positions = np.zeros(num_joints)
    
    def move_joint(self, joint_id, angle):
        """Move a specific joint to target angle"""
        if 0 <= joint_id < self.num_joints:
            self.joint_positions[joint_id] = angle
        else:
            raise ValueError(f"Invalid joint ID: {joint_id}")
    
    def get_end_effector_position(self):
        """Calculate end effector position using forward kinematics"""
        # Simplified example
        return self.joint_positions.sum()

# Usage
arm = RobotArm(num_joints=6)
arm.move_joint(0, np.pi/4)
print(f"Joint positions: {arm.joint_positions}")
```

### 3. Working with Matrices and Transformations

Understanding transformations is crucial for robotics:

```python
def create_transform_matrix(translation, rotation):
    """Create 4x4 homogeneous transformation matrix"""
    T = np.eye(4)
    T[:3, :3] = rotation
    T[:3, 3] = translation
    return T

# Example: Transform from robot base to end effector
translation = np.array([0.5, 0.2, 0.3])
rotation = np.eye(3)  # No rotation for simplicity
T_base_to_ee = create_transform_matrix(translation, rotation)
print("Transformation matrix:")
print(T_base_to_ee)
```

## Practice Exercises

:::tip Exercise 1: Vector Operations

Write a function that calculates the dot product and cross product of two 3D vectors without using NumPy's built-in functions.

:::

:::tip Exercise 2: Robot Joint Controller

Create a class that manages multiple robot joints with position limits and velocity constraints.

:::

## Key Takeaways

- NumPy is essential for efficient numerical computations
- OOP helps organize complex robotics systems
- Matrix operations are fundamental for robot kinematics
- Understanding transformations is critical for spatial reasoning

## Next Steps

Now that you have Python fundamentals under your belt, let's explore [reinforcement learning basics](/docs/category/reinforcement-learning) to train intelligent agents!
