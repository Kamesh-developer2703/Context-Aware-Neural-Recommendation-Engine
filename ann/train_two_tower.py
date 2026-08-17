import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from dataset import RecommendationDataset
from model import TwoTowerModel


# ============================================
# Device
# ============================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("Using device:", device)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================
# Dataset
# ============================================

dataset = RecommendationDataset()

loader = DataLoader(
    dataset,
    batch_size=256,
    shuffle=True,
    num_workers=0,
    pin_memory=torch.cuda.is_available()
)


# ============================================
# Model
# ============================================

model = TwoTowerModel().to(device)


# ============================================
# Loss
# ============================================

criterion = nn.MSELoss()


# ============================================
# Optimizer
# ============================================

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================
# Training
# ============================================

epochs = 3

print("\nTraining Started...\n")


for epoch in range(epochs):

    model.train()

    total_loss = 0.0

    for customer, article, label in loader:

        customer = customer.to(
            device,
            non_blocking=True
        )

        article = article.to(
            device,
            non_blocking=True
        )

        label = label.to(
            device,
            non_blocking=True
        )

        # ------------------------------------
        # Forward
        # ------------------------------------

        output = model(
            customer,
            article
        )

        # Convert labels:
        #
        # positive = +1
        # negative = -1
        #
        target = (
            label * 2
        ) - 1

        loss = criterion(
            output,
            target
        )

        # ------------------------------------
        # Backpropagation
        # ------------------------------------

        optimizer.zero_grad(
            set_to_none=True
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()


    average_loss = (
        total_loss /
        len(loader)
    )

    print(
        f"Epoch {epoch + 1}/{epochs} "
        f"Loss: {average_loss:.6f}"
    )


# ============================================
# Save
# ============================================

torch.save(
    model.state_dict(),
    "models/two_tower_model_v2.pth"
)

print(
    "\nModel Saved Successfully!"
)