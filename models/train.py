import os
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from models.dataset import RecommendationDataset
from models.two_tower_model import TwoTowerModel


def train():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using Device:", device)

    dataset = RecommendationDataset()

    dataloader = DataLoader(
        dataset,
        batch_size=256,
        shuffle=True
    )

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

    epochs = 20
    history = []

    for epoch in range(epochs):

        model.train()

        total_loss = 0
        correct = 0
        total = 0

        for users, items, labels in dataloader:

            users = users.to(device)
            items = items.to(device)
            labels = labels.float().to(device)

            optimizer.zero_grad()

            outputs = model(users, items)

            loss = criterion(outputs, labels)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

            predictions = (torch.sigmoid(outputs) >= 0.5).float()

            correct += (predictions == labels).sum().item()
            total += labels.size(0)

        avg_loss = total_loss / len(dataloader)
        accuracy = 100 * correct / total

        history.append([epoch + 1, avg_loss, accuracy])

        print(
            f"Epoch {epoch+1}/{epochs} | "
            f"Loss: {avg_loss:.4f} | "
            f"Accuracy: {accuracy:.2f}%"
        )

    os.makedirs("outputs", exist_ok=True)

    history_df = pd.DataFrame(
        history,
        columns=["Epoch", "Loss", "Accuracy"]
    )

    history_df.to_csv(
        "outputs/training_history.csv",
        index=False
    )

    os.makedirs("saved_models", exist_ok=True)

    torch.save(
        model.state_dict(),
        "saved_models/two_tower_model_day11.pth"
    )

    print("✅ Training completed successfully.")
    print("✅ Model saved.")
    print("✅ Training history saved.")


if __name__ == "__main__":
    train()