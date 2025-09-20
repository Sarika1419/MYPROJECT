import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# =================================================
# Load dataset
# =================================================
df = pd.read_csv("D:/MYPROJECT/processed_skincare_dataset1.csv")

# Normalize column names (remove spaces, lowercase, underscores)
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

print("Available columns:", df.columns.tolist())

# =================================================
# Encode categorical features (except target columns)
# =================================================
label_encoders = {}
target_cols = ["morning_routine", "night_routine",
               "suggested_morning_routine", "suggested_evening_routine"]

for col in df.select_dtypes(include=["object"]).columns:
    if col not in target_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# =================================================
# Train helper function
# =================================================
def train_and_save(X, y, filename):
    if len(y) == 0:
        print(f"⚠️ Skipping {filename}, no data available!")
        return
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    pickle.dump(model, open(filename, "wb"))
    print(f"✅ Saved {filename}")

# =================================================
# New Users
# =================================================
df_new = df[df["user_type"] == "new_user"]
X_new = df_new.drop(columns=target_cols + ["user_type"], errors="ignore")

train_and_save(X_new, df_new["morning_routine"], "new_morning.pkl")
train_and_save(X_new, df_new["night_routine"], "new_evening.pkl")

# =================================================
# Existing Users
# =================================================
df_exist = df[df["user_type"] == "existing_user"]
X_exist = df_exist.drop(columns=target_cols + ["user_type"], errors="ignore")

train_and_save(X_exist, df_exist["suggested_morning_routine"], "exist_morning.pkl")
train_and_save(X_exist, df_exist["suggested_evening_routine"], "exist_evening.pkl")
