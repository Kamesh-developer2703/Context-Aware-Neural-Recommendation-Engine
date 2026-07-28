import torch.nn as nn


class QueryTower(nn.Module):

    def __init__(self, input_dim, embedding_dim=64):
        super(QueryTower, self).__init__()

        self.network = nn.Sequential(

            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, embedding_dim)

        )

    def forward(self, x):
        return self.network(x)