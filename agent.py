import flappy_bird_gymnasium
import gymnasium as gym
import torch

from dqn import DQN
from replay import ReplayBuffer

env = gym.make("FlappyBird-v0", render_mode="human", use_lidar=True)

obs, _ = env.reset()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:
    def run(self, is_training: bool = False):
        env = gym.make("FlappyBird-v0", render_mode="human", use_lidar=True)
        num_states = env.observation_space.shape[0]
        num_actions = env.action_space.n

        policy = DQN(num_states, num_actions).to(device)
        obs, _ = env.reset()

        if is_training:
            replay_memory = ReplayBuffer(10000)
        
        episode_per_reward = []

        for episode in range(1000):
            state = env.reset()
            terminated = False
            episode_reward = 0.0
            print(f"Episode {episode + 1}/1000")
            while not terminated:
                # Next action
                action = env.action_space.sample()

                # Processing
                new_state, reward, terminated, _, info = env.step(action)

                episode_reward += reward

                if is_training:
                    replay_memory.push((state, action, reward, new_state, terminated))

                state = new_state
        
            episode_per_reward.append(episode_reward)
        env.close()

if __name__ == "__main__":
    agent = Agent()
    agent.run(is_training=True)