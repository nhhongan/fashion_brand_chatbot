import flappy_bird_gymnasium
import gymnasium as gym

env = gym.make("FlappyBird-v0", render_mode="human", use_lidar=True)

obs, _ = env.reset()
while True:
    # Next action
    action = env.action_space.sample()

    # Processing
    obs, reward, terminate, _, info = env.step(action)

    # Termination
    if terminate:
        break

env.close()