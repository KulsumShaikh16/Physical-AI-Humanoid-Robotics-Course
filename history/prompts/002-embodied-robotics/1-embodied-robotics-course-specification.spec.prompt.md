---
id: 1
title: Embodied Robotics Course Specification
stage: spec
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-embodied-robotics
branch: 002-embodied-robotics
user: user
command: /sp.specify
labels: ["specification", "embodied-ai", "robotics", "course"]
links:
  spec: specs/002-embodied-robotics/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-embodied-robotics/spec.md
  - specs/002-embodied-robotics/checklists/requirements.md
tests: []
---

## Prompt

Overview:
This course bridges the gap between the digital brain and the physical body by providing students with hands-on experience in designing, simulating, and deploying humanoid robots capable of natural human interactions using ROS 2, Gazebo, and NVIDIA Isaac. Students will explore the field of embodied AI, learning how AI systems can function and interact in the physical world by integrating various middleware, perception models, reinforcement learning, and voice-based interactions.

Target Audience:
Students with foundational knowledge of AI and robotics, looking to advance their understanding of embodied AI and humanoid robots.

Course Duration: 13 weeks (Capstone project included)

Modules & High-Level Details:
Module 1: The Robotic Nervous System (ROS 2)

Focus: Middleware for robot control

Key Topics:

ROS 2 Architecture (Nodes, Topics, Services, Actions)

Python Integration with ROS 2 (rclpy)

URDF for Humanoid Robots

Learning Outcomes:

Understanding the architecture of ROS 2 and how it manages robot communication

Practical experience creating and deploying robots using ROS 2

Module 2: The Digital Twin (Gazebo & Unity)

Focus: Physics simulation and environment building

Key Topics:

Gazebo Simulation Setup (gravity, collisions, sensor integration)

Unity Integration for High-Fidelity Rendering and Visualization

Simulating Sensors (LiDAR, Depth Cameras, IMUs)

Learning Outcomes:

Ability to simulate robots and environments with accurate physics

Implement sensor simulations for robotic perception in virtual environments

Module 3: The AI-Robot Brain (NVIDIA Isaac™)

Focus: Advanced perception and robot training

Key Topics:

NVIDIA Isaac Sim and Synthetic Data Generation

Visual SLAM (VSLAM) for Autonomous Navigation

Path Planning with Nav2 for Humanoid Robots

Reinforcement Learning for Robot Control

Learning Outcomes:

Understand advanced robot perception and control systems with NVIDIA Isaac

Implement AI-powered navigation and reinforcement learning in simulated environments

Module 4: Vision-Language-Action (VLA)

Focus: The convergence of LLMs and Robotics

Key Topics:

Voice-to-Action Integration (OpenAI Whisper)

Cognitive Planning with LLMs to Translate Voice Commands into Actions

Capstone Project: Fully Autonomous Humanoid Robot

Learning Outcomes:

Integrate natural language processing into robot control systems

Create an autonomous humanoid robot capable of executing voice commands and interacting with its environment

Capstone Project:

The course culminates in a Capstone project where students will develop a fully autonomous humanoid robot. The robot will be capable of receiving and understanding voice commands, navigating obstacles, identifying objects using computer vision, and performing manipulations in real-world or simulated environments.

Capstone Goals:

Build and deploy a humanoid robot with cognitive planning and sensory perception capabilities.

Demonstrate robot control through both simulated and real-world actions.

Use voice commands to trigger actions such as navigating paths, manipulating objects, and interacting with users.

Assessment Criteria:

ROS 2 Package Development: Practical application of robot control via ROS 2.

Gazebo Simulation Implementation: Set up and manage complex simulated environments.

Isaac-based Perception Pipeline: Develop perception models for real-time decision-making.

Capstone Project: Demonstrate a fully autonomous humanoid robot capable of multi-modal interaction.

Hardware Requirements:
1. The "Digital Twin" Workstation (Required per Student)

GPU: NVIDIA RTX 4070 Ti (12GB VRAM) or higher

CPU: Intel Core i7 (13th Gen+) or AMD Ryzen 9

RAM: 64 GB DDR5

OS: Ubuntu 22.04 LTS

2. The "Physical AI" Edge Kit

Brain: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)

Vision: Intel RealSense D435i or D455
Balance: USB IMU (BNO055)

Voice Interface: USB Microphone/Speaker array (e.g., ReSpeaker)

3. Robot Lab (Optional)

Proxy: Unitree Go2 Edu (~$1,800 - $3,000)

Miniature Humanoid: Unitree G1 (~$16k) or Robotis OP3 (~$12k)

Premium: Unitree G1 Humanoid (~$30k)

Cloud-Native Option (High OpEx):

Cloud Workstations: AWS g5.2xlarge or g6e.xlarge (for remote simulation)

Local "Bridge" Hardware: NVIDIA Jetson Kit (for physical deployment)

Timeline:

Duration: 13 Weeks

Weekly Commitment: 10-15 hours

Capstone Deadline: Week 13 (Final Presentation and Project Submission)

Success Criteria:

Practical understanding and application of ROS 2 for robot control.

Proficiency in simulating robots using Gazebo and Unity.

Advanced AI applications using NVIDIA Isaac and reinforcement learning.

Development of a fully autonomous humanoid robot capable of voice command integration and physical interaction.

## Response snapshot

Successfully generated and validated the specification for the 'Embodied AI and Humanoid Robotics Course'. The spec is available at `specs/002-embodied-robotics/spec.md` and the quality checklist at `specs/002-embodied-robotics/checklists/requirements.md`. All quality checks passed. The feature is ready for planning (`/sp.plan`).

## Outcome

- ✅ Impact: Specification for a new course feature.
- 🧪 Tests: Specification quality checklist passed.
- 📁 Files: Created `specs/002-embodied-robotics/spec.md` and `specs/002-embodied-robotics/checklists/requirements.md`.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Manual PHR creation due to script execution issue on `win32`. Confirmed successful directory creation and file writing using agent-native tools.

## Evaluation notes (flywheel)

- Failure modes observed: Bash script `.specify/scripts/bash/create-phr.sh` failed to execute on `win32` platform.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Investigate robust cross-platform shell script execution or agent-native alternatives for utility scripts.
