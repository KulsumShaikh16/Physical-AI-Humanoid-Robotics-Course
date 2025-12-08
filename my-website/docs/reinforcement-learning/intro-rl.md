---
sidebar_position: 1
---

# Introduction to Reinforcement Learning

Reinforcement Learning (RL) is the foundation of intelligent robot behavior. Unlike supervised learning, RL agents learn through trial and error, receiving rewards for good actions and penalties for poor ones.

## The RL Framework

### Core Components

Every RL problem consists of:

1. **Agent** – The learner/decision maker (your robot)
2. **Environment** – The world the agent interacts with
3. **State** – Current situation of the environment
4. **Action** – What the agent can do
5. **Reward** – Feedback signal indicating how good an action was

### The Agent-Environment Loop

```
State (s_t) → Agent → Action (a_t) → Environment → Reward (r_t) + State (s_{t+1})
                ↑                                              ↓
                └──────────────────────────────────────────────┘
```

## A Simple Example: Robot Navigation

Let's implement a basic grid world where a robot learns to navigate to a goal:

```python
import numpy as np

class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.agent_pos = [0, 0]
        self.goal_pos = [size-1, size-1]
    
    def reset(self):
        """Reset environment to initial state"""
        self.agent_pos = [0, 0]
        return self.get_state()
    
    def get_state(self):
        """Return current state"""
        return tuple(self.agent_pos)
    
    def step(self, action):
        """
        Take action and return (next_state, reward, done)
        Actions: 0=up, 1=right, 2=down, 3=left
        """
        moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        new_pos = [
            self.agent_pos[0] + moves[action][0],
            self.agent_pos[1] + moves[action][1]
        ]
        
        # Check boundaries
        if 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size:
            self.agent_pos = new_pos
        
        # Calculate reward
        if self.agent_pos == self.goal_pos:
            reward = 10.0
            done = True
        else:
            reward = -0.1  # Small penalty for each step
            done = False
        
        return self.get_state(), reward, done

# Test the environment
env = GridWorld(size=5)
state = env.reset()
print(f"Initial state: {state}")

# Take random actions
for _ in range(10):
    action = np.random.randint(0, 4)
    state, reward, done = env.step(action)
    print(f"State: {state}, Reward: {reward}, Done: {done}")
    if done:
        break
```

## Q-Learning Algorithm

Q-Learning is a fundamental RL algorithm that learns the value of taking actions in states:

```python
class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, 
                 discount_factor=0.95, epsilon=1.0):
        self.q_table = np.zeros((state_size, state_size, action_size))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
    
    def get_action(self, state):
        """Epsilon-greedy action selection"""
        if np.random.random() < self.epsilon:
            return np.random.randint(0, 4)  # Random action
        else:
            return np.argmax(self.q_table[state[0], state[1]])  # Best action
    
    def update(self, state, action, reward, next_state, done):
        """Update Q-value using Bellman equation"""
        current_q = self.q_table[state[0], state[1], action]
        
        if done:
            target_q = reward
        else:
            max_next_q = np.max(self.q_table[next_state[0], next_state[1]])
            target_q = reward + self.gamma * max_next_q
        
        # Q-learning update rule
        self.q_table[state[0], state[1], action] += self.lr * (target_q - current_q)
    
    def decay_epsilon(self):
        """Reduce exploration over time"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

# Train the agent
env = GridWorld(size=5)
agent = QLearningAgent(state_size=5, action_size=4)

episodes = 1000
for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    
    for step in range(100):
        action = agent.get_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        
        state = next_state
        total_reward += reward
        
        if done:
            break
    
    agent.decay_epsilon()
    
    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.3f}")
```

## Key Concepts

### Exploration vs. Exploitation

- **Exploration** – Trying new actions to discover better strategies
- **Exploitation** – Using known good actions to maximize reward
- **Epsilon-Greedy** – Balance between random (explore) and best (exploit) actions

### The Bellman Equation

The core of Q-learning:

```
Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]
```

Where:
- α = learning rate
- γ = discount factor
- r = reward
- s = current state, s' = next state
- a = action

## Practice Exercises

:::tip Exercise 1: Tune Hyperparameters

Experiment with different learning rates, discount factors, and epsilon decay rates. How do they affect learning speed?

:::

:::tip Exercise 2: Add Obstacles

Modify the GridWorld to include obstacles. The agent should learn to navigate around them!

:::

:::tip Exercise 3: Visualize Learning

Create a visualization showing how the Q-values evolve during training.

:::

## Next Steps

Now that you understand basic RL, let's explore [deep reinforcement learning](./deep-rl.md) where we use neural networks instead of Q-tables!
