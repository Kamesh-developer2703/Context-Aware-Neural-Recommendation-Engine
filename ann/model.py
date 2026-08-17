import torch
import torch.nn as nn
import torch.nn.functional as F


class TwoTowerModel(nn.Module):

    def __init__(self):

        super().__init__()

        # Customer Tower
        self.customer_tower = nn.Sequential(
            nn.Linear(9, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )

        # Article Tower
        self.article_tower = nn.Sequential(
            nn.Linear(9, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )

    def forward(self, customer, article):

        customer_embedding = self.customer_tower(customer)
        article_embedding = self.article_tower(article)

        # Normalize embeddings
        customer_embedding = F.normalize(
            customer_embedding,
            p=2,
            dim=1
        )

        article_embedding = F.normalize(
            article_embedding,
            p=2,
            dim=1
        )

        # Cosine similarity
        score = torch.sum(
            customer_embedding * article_embedding,
            dim=1
        )

        return score