import torch.nn as nn


class CandidateTower(nn.Module):

    def __init__(self, input_dim, embedding_dim=64):
        super(CandidateTower, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            nn.Linear(64, embedding_dim)
        )

    def forward(self, x):
        return self.network(x)