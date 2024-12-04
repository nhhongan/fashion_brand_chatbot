# Playing flappy bird with Reinforcement Learning

This is a simple implementation of the game Flappy Bird using Pygame. The game is controlled by a Reinforcement Learning agent that learns to play the game using the Q-learning algorithm.

## Installation

Install astral's uv:

`pip install uv`

To install the required packages, run the following command:

`uv sync` or `pip install -r requirements.txt`

## Usage

Run the program as training

`uv run agent.py --train` or `python agent.py --train`

Run the program as testing **ensure that there is flappybird-1.pth before running**

`uv run agent.py` or `python agent.py`