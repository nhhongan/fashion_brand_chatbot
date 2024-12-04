import argparse
from datetime import datetime, timedelta
import random
import flappy_bird_gymnasium
import gymnasium as gym
import numpy as np
import torch
from torch import nn
from dqn import DQN
from replay import ReplayBuffer
import yaml
import matplotlib.pyplot as plt
import matplotlib
import os

# For printing date and time
DATE_FORMAT = "%m-%d %H:%M:%S"
RUN_DIR = "runs"
os.makedirs(RUN_DIR, exist_ok=True)

matplotlib.use("Agg")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:
    def __init__(self, hyper_set):
        with open("hyperparameters.yaml", "r") as f:
            _hyperpar = yaml.safe_load(f)
            _hyperpar = _hyperpar[hyper_set]

        ## HYPERPARAMETERS ##
        self.env_id = _hyperpar["env_id"]
        self.replay_buffer_size = _hyperpar["replay_buffer_size"]
        self.minibatch_size = _hyperpar["minibatch_size"]
        self.epsilon_initial = _hyperpar["epsilon_initial"]
        self.epsilon_final = _hyperpar["epsilon_final"]
        self.epsilon_decay = _hyperpar["epsilon_decay"]
        self.update_target_frequency = _hyperpar["update_target_frequency"]
        self.discount_factor: float = _hyperpar["discount_factor"]
        self.learning_rate: float = _hyperpar["learning_rate"]
        self.max_reward: float = _hyperpar["max_reward"]
        self.max_episode: int = _hyperpar["max_episode"]
        ## NEURAL NETWORK ##    
        self.loss_fn = nn.MSELoss()
        self.optimizer: torch.optim.Optimizer = None
        self.hidden_dim = _hyperpar["hidden_dim"]

        ## Path to Run info
        self.LOG_FILE = os.path.join(RUN_DIR, f"{hyper_set}.log")
        self.MODEL_FILE = os.path.join(RUN_DIR, f"{hyper_set}.pth")
        self.GRAPH_FILE = os.path.join(RUN_DIR, f"{hyper_set}.png")

    def optimize(self, batch, policy_dqn: DQN, target_dqn: DQN):
        state, action, reward, new_state, terminated = zip(*batch)

        states = torch.stack(state)
        actions = torch.stack(action)
        rewards = torch.stack(reward)
        new_states = torch.stack(new_state)
        terminated = torch.tensor(terminated, dtype=torch.float32).to(device)

        with torch.no_grad():
            target_q = rewards + (1-terminated) *  self.discount_factor * target_dqn(new_states).max(dim=1)[0]

        current_q = policy_dqn(states).gather(dim=1, index=actions.unsqueeze(dim=1)).squeeze()
        loss = self.loss_fn(target_q, current_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
    def save_graph(self, reward_per_episode, epsilon_history):
        # Save plots
        fig = plt.figure(1)

        # Plot average reward vs episodes
        mean_rewards = np.zeros(len(reward_per_episode))
        for x in range(len(reward_per_episode)):
            mean_rewards[x] = np.mean(reward_per_episode[max(0, x-99):(x+1)])
        plt.subplot(121) # 1 row, 2 columns, 1st subplot
        plt.ylabel("Average reward")
        plt.plot(mean_rewards)

        # Plot epsilon decay vs episodes
        plt.subplot(122) # 1 row, 2 columns, 2nd subplot
        plt.ylabel("Epsilon")
        plt.plot(epsilon_history)

        plt.subplots_adjust(wspace=1, hspace=1)

        plt.savefig(self.GRAPH_FILE)
        plt.close(fig)

    def run(self, is_training: bool = False, is_render: bool = False):
        ## START TRAINING ##
        if is_training:
            start_time = datetime.now()
            last_graph_update_time = start_time

            log_message = f"{start_time.strftime(DATE_FORMAT)}: Training started..."
            print(log_message)
            with open(self.LOG_FILE, "a") as f:
                f.write(log_message + "\n")

        env = gym.make(self.env_id, render_mode="human" if is_render else None)
        num_states = env.observation_space.shape[0]
        num_actions = env.action_space.n

        policy = DQN(num_states, num_actions, self.hidden_dim).to(device)
        obs, _ = env.reset()

        if is_training:
            replay_memory = ReplayBuffer(self.replay_buffer_size)
            epsilon = self.epsilon_initial
            target_dqn = DQN(num_states, num_actions, self.hidden_dim).to(device)
            target_dqn.load_state_dict(policy.state_dict())
            step_count = 0
            self.optimizer = torch.optim.Adam(policy.parameters(), lr = self.learning_rate)
            best_reward = -9999
            epsilon_history = [epsilon]
        else:
            policy.load_state_dict(torch.load(self.MODEL_FILE, map_location=device))
            policy.eval()

        episode_per_reward = []

        for episode in range(self.max_episode):
            state, _ = env.reset()
            state = torch.tensor(state, dtype=torch.float32).to(device)
            terminated = False
            episode_reward = 0.0
            ### UNTIL THE GAME IS OVER
            while (not terminated and episode_reward < self.max_reward):
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
            if is_training:
                if episode_reward > best_reward:
                    log_message = f"{datetime.now().strftime(DATE_FORMAT)}: New best reward {episode_reward:0.1f} ({(episode_reward-best_reward)/best_reward*100:0.1f}%) at episode {episode+1}"
                    print(log_message)
                    with open(self.LOG_FILE, 'a') as f:
                        f.write(log_message + "\n")
                    torch.save(policy.state_dict(), self.MODEL_FILE)
                    best_reward = episode_reward

                # Update graph every x seconds
                current_time = datetime.now()
                if current_time - last_graph_update_time > timedelta(seconds=10):
                    self.save_graph(episode_per_reward, epsilon_history)
                    last_graph_update_time = current_time

                epsilon = max(self.epsilon_final, epsilon * self.epsilon_decay)
                epsilon_history.append(epsilon)
                if len(replay_memory) > self.minibatch_size:
                    minibatch = replay_memory.sample(self.minibatch_size)
                    self.optimize(minibatch, policy, target_dqn)

                if episode % self.update_target_frequency == 0:
                    target_dqn.load_state_dict(policy.state_dict())

                if episode % 100 == 0:
                    print(f"Episode {episode + 1}/{self.max_episode}, Reward: {episode_reward:.2f}, Epsilon: {epsilon:.2f}")
        log_message = f"{datetime.now().strftime(DATE_FORMAT)}: Training ended..."
        print(log_message)
        with open(self.LOG_FILE, "a") as f:
            f.write(log_message + "\n")
        env.close()
        return episode_per_reward

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flappy Bird DQN")
    parser.add_argument("--hyper_set", type=str, default="flappybird-1")
    parser.add_argument("--train", action="store_true", help="Train the model")
    arg = parser.parse_args()

    agent = Agent("flappybird-1")
    if arg.train:
        episode_reward = agent.run(is_training=True, is_render=False)
    else:
        episode_reward = agent.run(is_training=False, is_render=True)
