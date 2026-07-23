import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from dataset import RecommendationDataset
from model import TwoTowerModel


dataset = RecommendationDataset()

loader = DataLoader(
    dataset,
    batch_size=256,
    shuffle=True
)

model = TwoTowerModel()

criterion = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 5

print("\nTraining Started...\n")

for epoch in range(epochs):

    total_loss = 0

    for customer, article, label in loader:

        optimizer.zero_grad()

        output = model(customer, article)

        loss = criterion(output, label)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch {epoch+1}/{epochs}  Loss : {total_loss:.4f}"
    )

torch.save(
    model.state_dict(),
    "models/two_tower_model_v2.pth"
)

print("\nModel Saved Successfully!")