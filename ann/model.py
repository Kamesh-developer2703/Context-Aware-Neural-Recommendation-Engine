import torch
import torch.nn as nn


class TwoTowerModel(nn.Module):

    def __init__(self):

        super().__init__()

        # Customer Tower (5 features)
        self.customer_tower = nn.Sequential(
            nn.Linear(5, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )

        # Article Tower (9 features)
        self.article_tower = nn.Sequential(
            nn.Linear(9, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )

    def forward(self, customer, article):

        customer_embedding = self.customer_tower(customer)
        article_embedding = self.article_tower(article)

        score = torch.sum(
            customer_embedding * article_embedding,
            dim=1
        )

        return score