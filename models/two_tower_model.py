import torch
import torch.nn as nn

from models.query_tower import QueryTower
from models.candidate_tower import CandidateTower


class TwoTowerModel(nn.Module):

    def __init__(self, user_dim, item_dim, embedding_dim=64):
        super(TwoTowerModel, self).__init__()

        self.query_tower = QueryTower(
            input_dim=user_dim,
            embedding_dim=embedding_dim
        )

        self.candidate_tower = CandidateTower(
            input_dim=item_dim,
            embedding_dim=embedding_dim
        )

    def forward(self, user_features, item_features):

        user_embedding = self.query_tower(user_features)
        item_embedding = self.candidate_tower(item_features)

        score = torch.sum(
            user_embedding * item_embedding,
            dim=1
        )

        return score