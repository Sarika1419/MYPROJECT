# train_new_user_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("D:/MYPROJECT/data/large_skincare_users_dataset_with_age.csv")
# Define features and targets
X_columns = [
    "Age", "Gender", "SkinType", "Redness", "WaterIntake",
    "DietType", "SunExposure", "UsesSPF", "NaturalRemedyUsed",
    "CleanseFreq", "WashWaterTemp", "SleepHours",
    "StressFreq", "AwareOfVitaminE", "TriedDIY"
]
y_morning = df["MorningRoutine"]
y_evening = df["EveningRoutine"]

# Encode categorical variables
X_encoded = pd.get_dummies(df[X_columns])

# Train models
morning_model = RandomForestClassifier()
evening_model = RandomForestClassifier()

morning_model.fit(X_encoded, y_morning)
evening_model.fit(X_encoded, y_evening)

# Save models
pickle.dump(morning_model, open("new_user_morning_model.pkl", "wb"))
pickle.dump(evening_model, open("new_user_evening_model.pkl", "wb"))

print("✅ Models trained and saved successfully!")
