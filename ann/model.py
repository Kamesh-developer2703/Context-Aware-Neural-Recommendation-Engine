import torch
import torch.nn as nn


class Tower(nn.Module):

    def __init__(self, input_size):

        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size,64),
            nn.ReLU(),

            nn.Linear(64,32),
            nn.ReLU(),

            nn.Linear(32,16)
        )

    def forward(self,x):

        return self.network(x)


class TwoTowerModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.user_tower = Tower(3)
        self.item_tower = Tower(3)

    def forward(self,user,item):

        user_embedding = self.user_tower(user)

        item_embedding = self.item_tower(item)

        score = (user_embedding * item_embedding).sum(dim=1)

        return score