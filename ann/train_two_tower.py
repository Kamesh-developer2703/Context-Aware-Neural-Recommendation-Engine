import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from dataset import RecommendationDataset
from model import TwoTowerModel

dataset = RecommendationDataset()

loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

model = TwoTowerModel()

loss_fn = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 5

for epoch in range(epochs):

    total_loss = 0

    for user,item,label in loader:

        prediction = model(user,item)

        loss = loss_fn(prediction,label)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} Loss : {total_loss:.4f}")

torch.save(
    model.state_dict(),
    "models/two_tower_model.pth"
)

print("\nModel Saved Successfully!")