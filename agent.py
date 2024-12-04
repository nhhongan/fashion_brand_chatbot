import random
import flappy_bird_gymnasium
import gymnasium as gym
import torch
from torch import nn
from dqn import DQN
from replay import ReplayBuffer
import yaml
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:
    def __init__(self, hyper_set):
        with open("hyperparameters.yaml", "r") as f:
            _hyperpar = yaml.safe_load(f)
            _hyperpar = _hyperpar[hyper_set]
        self.env_id = _hyperpar["env_id"]
        self.replay_buffer_size = _hyperpar["replay_buffer_size"]
        self.minibatch_size = _hyperpar["minibatch_size"]
        self.epsilon_initial = _hyperpar["epsilon_initial"]
        self.epsilon_final = _hyperpar["epsilon_final"]
        self.epsilon_decay = _hyperpar["epsilon_decay"]
        self.update_target_frequency = _hyperpar["update_target_frequency"]
        self.discount_factor: float = _hyperpar["discount_factor"]
        self.learning_rate: float = _hyperpar["learning_rate"]
        self.loss_fn = nn.MSELoss()
        self.optimizer: torch.optim.Optimizer = None

    def optimize(self, batch, policy_dqn: DQN, target_dqn: DQN):
        state, action, reward, new_state, terminated = zip(*batch)

        states = torch.stack(state)
        actions = torch.stack(action)
        rewards = torch.stack(reward)
        new_states = torch.stack(new_state)
        terminated = torch.tensor(terminated, dtype=torch.float32).to(device)

        with torch.no_grad():
            target_q = (1-terminated) * rewards  + self.discount_factor * target_dqn(new_states).max(dim=1)[0]

        current_q = policy_dqn(states).gather(dim=1, index=actions.unsqueeze(dim=1)).squeeze()
        loss = self.loss_fn(target_q, current_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
    def run(self, is_training: bool = False, is_render: bool = False):
        env = gym.make(self.env_id, render_mode="human" if is_render else None, use_lidar=True)
        num_states = env.observation_space.shape[0]
        num_actions = env.action_space.n

        policy = DQN(num_states, num_actions).to(device)
        obs, _ = env.reset()

        if is_training:
            replay_memory = ReplayBuffer(self.replay_buffer_size)
            epsilon = self.epsilon_initial
            target_dqn = DQN(num_states, num_actions).to(device)
            target_dqn.load_state_dict(policy.state_dict())
            step_count = 0
            self.optimizer = torch.optim.Adam(policy.parameters(), lr = self.learning_rate)
        episode_per_reward = []

        for episode in range(1000):
            state, _ = env.reset()
            state = torch.tensor(state, dtype=torch.float32).to(device)
            terminated = False
            episode_reward = 0.0
            print(f"Episode {episode + 1}/1000")
            ### UNTIL THE GAME IS OVER
            while not terminated:
                # Next action
                if is_training and random.random() < epsilon:
                    action = env.action_space.sample()
                    action = torch.tensor(action, dtype=torch.int64, device=device)
                else:
                    # Q-values -> Select index of the highest q-value -> Get the action
                    with torch.no_grad():
                        action = policy(state.unsqueeze(0)).squeeze().argmax()

                # Processing
                new_state, reward, terminated, _, info = env.step(action.item())

                episode_reward += reward
                new_state = torch.tensor(new_state, dtype=torch.float32).to(device)
                reward = torch.tensor(reward, dtype=torch.float32).to(device)

                if is_training:
                    replay_memory.push((state, action, reward, new_state, terminated))
                    step_count += 1

                state = new_state
        
            episode_per_reward.append(episode_reward)
            epsilon = max(self.epsilon_final, epsilon * self.epsilon_decay)
            if is_training:
                if len(replay_memory) > self.minibatch_size:
                    minibatch = replay_memory.sample(self.minibatch_size)
                    self.optimize(minibatch, policy, target_dqn)

                if episode % self.update_target_frequency == 0:
                    target_dqn.load_state_dict(policy.state_dict())

            if episode % 100 == 0:
                print(f"Episode {episode + 1}/{1000}, Reward: {episode_reward}, Epsilon: {epsilon}")

        env.close()
        return episode_per_reward

if __name__ == "__main__":
    agent = Agent("flappybird-1")
    episode_reward = agent.run(is_training=True, is_render=False)
    plt.plot(episode_reward)
    plt.show()
    