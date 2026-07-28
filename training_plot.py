import pandas as pd
import matplotlib.pyplot as plt

history = pd.read_csv("outputs/training_history.csv")

plt.figure(figsize=(8,5))
plt.plot(history["Epoch"], history["Loss"], marker="o")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.grid()

plt.savefig("outputs/loss_curve.png")
plt.close()


plt.figure(figsize=(8,5))
plt.plot(history["Epoch"], history["Accuracy"], marker="o")
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")
plt.title("Training Accuracy")
plt.grid()

plt.savefig("outputs/accuracy_curve.png")
plt.close()

print("Graphs Saved Successfully!")