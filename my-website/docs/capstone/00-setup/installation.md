---
sidebar_position: 1
---

# Installation Guide

This guide will walk you through setting up the complete development environment for the Autonomous Humanoid Robot Capstone project.

**Estimated Time**: 2 hours  
**Difficulty**: Intermediate

## Prerequisites

- Ubuntu 22.04 LTS (clean installation recommended)
- Stable internet connection
- At least 50GB free disk space
- Administrator (sudo) access

> **Note**: While this project can run on lower-spec hardware, we recommend the specifications listed in the [main README](../../capstone/index.md#🛠️-technologies-used) for optimal performance.

## Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install ROS 2 Humble

### Add ROS 2 Repository

```bash
# Install prerequisites
sudo apt install -y software-properties-common curl gnupg lsb-release

# Add ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add ROS 2 repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update package list
sudo apt update
```

### Install ROS 2 Packages

```bash
# Install ROS 2 Humble Desktop (includes RViz, demos, tutorials)
sudo apt install -y ros-humble-desktop

# Install additional ROS 2 packages
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-moveit \
  ros-humble-moveit-visual-tools \
  ros-humble-moveit-servo \
  ros-humble-robot-localization \
  ros-humble-slam-toolbox
```

### Setup ROS 2 Environment

```bash
# Source ROS 2 setup (add to ~/.bashrc for automatic sourcing)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify installation
ros2 --version
# Expected output: ros2 cli version humble
```

## Step 3: Install Gazebo Classic 11

```bash
# Gazebo 11 should be installed with ros-humble-gazebo-ros-pkgs
# Verify installation
gazebo --version

# If not installed, manually install:
sudo apt install -y gazebo libgazebo-dev
```

## Step 4: Install Development Tools

### Build Tools

```bash
# Install colcon (ROS 2 build tool)
sudo apt install -y python3-colcon-common-extensions

# Install rosdep (dependency management)
sudo apt install -y python3-rosdep
sudo rosdep init
rosdep update
```

### Python Development Tools

```bash
# Install Python 3.10+ and pip
sudo apt install -y python3-pip python3-dev python3-venv

# Upgrade pip
python3 -m pip install --upgrade pip
```

## Step 5: Install Python Dependencies

Navigate to the project directory and install required Python packages:

```bash
# Navigate to project root
cd ~/path/to/autonomous-humanoid

# Install Python dependencies
pip3 install -r requirements.txt
```

### Key Packages Installed:
- **OpenCV**: Computer vision library
- **Ultralytics (YOLOv8)**: Object detection
- **PyTorch**: Deep learning framework
- **OpenAI Whisper**: Speech recognition
- **NumPy, SciPy**: Scientific computing

## Step 6: Install NVIDIA Isaac Sim (Optional)

> **Required only if**: You have an NVIDIA GPU and want to use Isaac for advanced vision processing

### Prerequisites
- NVIDIA GPU with 6GB+ VRAM
- NVIDIA drivers installed (version 525+)
- CUDA 11.8 or later

### Installation

1. **Install NVIDIA Container Toolkit** (for Docker-based Isaac):
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
         sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
         sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   ```

2. **Download Isaac Sim** from [NVIDIA website](https://developer.nvidia.com/isaac-sim)

3. **Follow NVIDIA's installation guide** for your specific setup

> **Alternative**: If you don't have an NVIDIA GPU, the YOLOv8 CPU fallback will be used automatically.

## Step 7: Setup Unity (Optional)

> **Required only if**: You want to explore Unity simulation as an alternative to Gazebo

1. **Install Unity Hub**:
   - Download from [Unity website](https://unity.com/download)
   - Install Unity 2022 LTS

2. **Install Unity Robotics Hub** packages:
   - Follow [Unity Robotics Hub guide](https://github.com/Unity-Technologies/Unity-Robotics-Hub)

## Step 8: Clone and Build the Project

### Clone Repository

```bash
# Create workspace directory
mkdir -p ~/robotics_ws
cd ~/robotics_ws

# Clone the repository (replace with actual repo URL)
git clone <repository_url> autonomous-humanoid
cd autonomous-humanoid
```

### Build ROS 2 Workspace

```bash
# Navigate to ROS 2 workspace
cd ros2_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build workspace
colcon build --symlink-install

# Source the workspace
source install/setup.bash

# Add to .bashrc for automatic sourcing
echo "source ~/robotics_ws/autonomous-humanoid/ros2_ws/install/setup.bash" >> ~/.bashrc
```

## Step 9: Download Pre-trained Models

### YOLOv8 Model

```bash
# Navigate to models directory
cd ~/robotics_ws/autonomous-humanoid/models

# Create YOLOv8 directory
mkdir -p yolov8

# Download YOLOv8 nano model (smallest, fastest)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O yolov8/yolov8n.pt

# Optional: Download larger models for better accuracy
# wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt -O yolov8/yolov8m.pt
```

### VLA Model (Optional)

If using RT-1/RT-2 VLA models:

```bash
# Follow instructions from the VLA model source
# Models are typically available through research institutions
# Or use the rule-based parser fallback (no download needed)
```

## Step 10: Verify Installation

Run these commands to verify everything is installed correctly:

```bash
# Check ROS 2
ros2 --version
ros2 pkg list | grep nav2

# Check Gazebo
gazebo --version

# Check Python packages
python3 -c "import cv2; import torch; import ultralytics; print('All Python packages OK')"

# Check workspace build
cd ~/robotics_ws/autonomous-humanoid/ros2_ws
colcon test
```

## Common Issues & Troubleshooting

### Issue: "ros2: command not found"

**Solution**: Source ROS 2 setup file:
```bash
source /opt/ros/humble/setup.bash
```

### Issue: Gazebo crashes on startup

**Solution**: Clear Gazebo cache:
```bash
rm -rf ~/.gazebo/cache
```

### Issue: colcon build fails with missing dependencies

**Solution**: Install dependencies with rosdep:
```bash
rosdep install --from-paths src --ignore-src -r -y
```

### Issue: PyTorch installation fails

**Solution**: Install CPU-only version:
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Permission denied errors

**Solution**: Add user to dialout group (for USB devices):
```bash
sudo usermod -a -G dialout $USER
# Logout and login again
```

## Next Steps

Once installation is complete:

1. ✅ Verify all tests pass
2. ✅ Launch a test simulation: `ros2 launch humanoid_bringup spawn_robot.launch.py`
3. ✅ Proceed to [Architecture Overview](../01-introduction/architecture.md)

---

## Installation Checklist

- [ ] Ubuntu 22.04 installed
- [ ] ROS 2 Humble installed and sourced
- [ ] Gazebo 11 working
- [ ] Python dependencies installed
- [ ] ROS 2 workspace built successfully
- [ ] YOLOv8 model downloaded
- [ ] (Optional) NVIDIA Isaac Sim installed
- [ ] (Optional) Unity 2022 LTS installed
- [ ] All verification tests pass

**Estimated total time**: ~2 hours

Need help? Check the [FAQ](../07-conclusion/faq.md) or open an issue!
