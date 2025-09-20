# train_returning_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("D:/MYPROJECT/data/large_skincare_users_dataset_with_age.csv")

# Keep only columns relevant to returning user
X = df[["FollowsRoutine", "Irritation",
        "SkinChange", "Improvement", "TriedDIY"]]
y_morning = df["MorningRoutine"]
y_evening = df["EveningRoutine"]

# Encode categorical variables
X_encoded = pd.get_dummies(X)

# Train separate models for morning & evening
morning_model = RandomForestClassifier()
evening_model = RandomForestClassifier()

morning_model.fit(X_encoded, y_morning)
evening_model.fit(X_encoded, y_evening)

# Save models
pickle.dump(morning_model, open("returning_morning_model.pkl", "wb"))
pickle.dump(evening_model, open("returning_evening_model.pkl", "wb"))

print("✅ Models trained and saved successfully!")
