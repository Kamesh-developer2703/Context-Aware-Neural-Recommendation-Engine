from models.dataset import RecommendationDataset
from models.two_tower_model import TwoTowerModel

dataset = RecommendationDataset()

user, item, label = dataset[0]

model = TwoTowerModel(
    user_dim=user.shape[0],
    item_dim=item.shape[0]
)

user = user.unsqueeze(0)
item = item.unsqueeze(0)

prediction = model(user, item)

print("User Shape :", user.shape)
print("Item Shape :", item.shape)
print("Prediction :", prediction)