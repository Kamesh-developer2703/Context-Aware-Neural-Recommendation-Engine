import faiss
import numpy as np

# Load FAISS index
index = faiss.read_index("ann/item_index.faiss")

# Load item embeddings
embeddings = np.load("embeddings/item_embeddings.npy")

# Use the first item embedding as a sample query
query = embeddings[0].reshape(1, -1)

# Number of recommendations
k = 10

# Search
distances, indices = index.search(query, k)

print("\nTop 10 Recommended Items\n")

for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
    print(f"{rank}. Item Index: {idx} | Distance: {dist:.4f}")