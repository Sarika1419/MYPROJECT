import pandas as pd

# Load dataset
df = pd.read_csv("D:/MYPROJECT/processed_skincare_dataset1.csv")

# Add user_type column manually
# For now, let’s assign randomly (50% new_user, 50% existing_user)
import numpy as np
df['user_type'] = np.random.choice(['new_user', 'existing_user'], size=len(df))

# Save again
df.to_csv("processed_skincare_dataset.csv", index=False)

print(df.head())
print(df['user_type'].value_counts())
