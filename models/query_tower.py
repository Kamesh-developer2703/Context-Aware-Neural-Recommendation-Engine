import torch.nn as nn


class QueryTower(nn.Module):

    def __init__(self, input_dim, embedding_dim=64):
        super(QueryTower, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),

            nn.Linear(32, 64),
            nn.ReLU(),

            nn.Linear(64, embedding_dim)
        )

    def forward(self, x):
        return self.network(x)