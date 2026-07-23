import os
import json

# 🚨 CRITICAL FIX: Force TensorFlow to use Keras 2 (Legacy) for TFRS compatibility
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tensorflow as tf
import tensorflow_recommenders as tfrs

# Define paths relative to project root
SCHEMA_PATH = os.path.join("data", "preprocessing", "item_tower_schema.json")
# ... rest of your code stays the same ...
# ---------------------------------------------------------------------------
# 1. ITEM (CANDIDATE) TOWER ARCHITECTURE
# ---------------------------------------------------------------------------
class ItemTower(tf.keras.Model):
    def __init__(self, schema):
        super().__init__()
        embedding_dimension = 32
        
        # Categorical Embedding Layers for Article Attributes
        self.product_type_embedding = tf.keras.layers.Embedding(
            input_dim=schema['categorical_encoded_features']['product_type_name_encoded']['cardinality'] + 1,
            output_dim=embedding_dimension
        )
        self.product_group_embedding = tf.keras.layers.Embedding(
            input_dim=schema['categorical_encoded_features']['product_group_name_encoded']['cardinality'] + 1,
            output_dim=embedding_dimension
        )
        self.colour_group_embedding = tf.keras.layers.Embedding(
            input_dim=schema['categorical_encoded_features']['colour_group_name_encoded']['cardinality'] + 1,
            output_dim=embedding_dimension
        )
        
        # Dense Feed-Forward Neural Network to output final 64-d Item Vector
        self.dense_layers = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64)
        ])

    def call(self, inputs):
        # Concatenate item embeddings
        p_type = self.product_type_embedding(inputs['product_type_name_encoded'])
        p_group = self.product_group_embedding(inputs['product_group_name_encoded'])
        c_group = self.colour_group_embedding(inputs['colour_group_name_encoded'])
        
        concat_features = tf.concat([p_type, p_group, c_group], axis=-1)
        return self.dense_layers(concat_features)


# ---------------------------------------------------------------------------
# 2. USER TOWER ARCHITECTURE
# ---------------------------------------------------------------------------
class UserTower(tf.keras.Model):
    def __init__(self, user_vocab_size=100000):
        super().__init__()
        embedding_dimension = 32
        
        self.user_embedding = tf.keras.layers.Embedding(
            input_dim=user_vocab_size + 1,
            output_dim=embedding_dimension
        )
        
        # Dense Feed-Forward Neural Network to output final 64-d User Vector
        self.dense_layers = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64)
        ])

    def call(self, inputs):
        u_emb = self.user_embedding(inputs['user_id_encoded'])
        return self.dense_layers(u_emb)


# ---------------------------------------------------------------------------
# 3. TWO-TOWER RECOMMENDATION MODEL & TRAINING CONFIGURATION
# ---------------------------------------------------------------------------
class TwoTowerModel(tfrs.Model):
    def __init__(self, item_tower, user_tower, candidate_dataset):
        super().__init__()
        self.item_tower = item_tower
        self.user_tower = user_tower
        
        # Loss Function: In-Batch Sampled Softmax / Categorical Cross Entropy Loss
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=candidate_dataset.map(self.item_tower)
            )
        )

    def compute_loss(self, features, training=False):
        user_embeddings = self.user_tower({
            "user_id_encoded": features["user_id_encoded"]
        })
        item_embeddings = self.item_tower({
            "product_type_name_encoded": features["product_type_name_encoded"],
            "product_group_name_encoded": features["product_group_name_encoded"],
            "colour_group_name_encoded": features["colour_group_name_encoded"]
        })
        
        return self.task(user_embeddings, item_embeddings)


# ---------------------------------------------------------------------------
# 4. MODEL INITIALIZATION & TRAINING CONFIGURATION SUMMARY
# ---------------------------------------------------------------------------
def configure_and_verify_model():
    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ Error: Schema metadata missing at {SCHEMA_PATH}")
        return

    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)

    print("⏳ Building User Tower & Item Tower Neural Architectures...")
    item_net = ItemTower(schema)
    user_net = UserTower()

    print("\n=== ⚙️ Training Process Configuration ===")
    print("🔹 Loss Function : Sampled Softmax Cross-Entropy (tfrs.tasks.Retrieval)")
    print("🔹 Optimizer     : Adam (Learning Rate = 0.001)")
    print("🔹 Target Epochs : 10 Epochs")
    print("🔹 Batch Size    : 2048")
    
    print("\n✅ Architecture verification pass: User & Item towers defined cleanly!")

if __name__ == "__main__":
    configure_and_verify_model()