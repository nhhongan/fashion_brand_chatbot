import torch
from torch import nn
from torch.nn import functional as F

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

        self.output = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.output(x)
    
if __name__ == "__main__":
    state_dim = 4
    action_dim = 2
    hidden_dim = 256
    state = torch.randn(1, state_dim)
    model = DQN(state_dim, action_dim, hidden_dim)
    print(model(state))