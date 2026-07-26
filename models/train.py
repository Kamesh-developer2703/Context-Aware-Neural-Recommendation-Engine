import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from models.dataset import RecommendationDataset
from models.two_tower_model import TwoTowerModel


def train():

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("Using Device :", device)

    # Dataset
    dataset = RecommendationDataset()

    dataloader = DataLoader(
        dataset,
        batch_size=256,
        shuffle=True
    )

    # Get feature dimensions
    user, item, label = dataset[0]

    model = TwoTowerModel(
        user_dim=user.shape[0],
        item_dim=item.shape[0]
    ).to(device)

    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    epochs = 10

    for epoch in range(epochs):

        model.train()

        total_loss = 0

        for users, items, labels in dataloader:

            users = users.to(device)
            items = items.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(users, items)

            loss = criterion(outputs, labels)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)

        print(
            f"Epoch [{epoch+1}/{epochs}] "
            f"Loss : {avg_loss:.4f}"
        )

    # Save model
    os.makedirs("saved_models", exist_ok=True)

    torch.save(
        model.state_dict(),
        "saved_models/two_tower_model.pth"
    )

    print("\nModel Saved Successfully!")


if __name__ == "__main__":
    train()