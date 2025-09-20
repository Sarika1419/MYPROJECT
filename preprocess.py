import pandas as pd

# Load dataset
df = pd.read_csv("D:/MYPROJECT/data/final_skincare_with_suggestions.csv")

# Function to assign user type
def assign_user_type(row):
    if pd.notna(row['Morning_Routine']) and pd.notna(row['Night_Routine']):
        return "new"
    elif pd.notna(row['Suggested Morning Routine']) and pd.notna(row['Suggested Evening Routine']):
        return "existing"
    else:
        return "unknown"

# Apply function
df['user_type'] = df.apply(assign_user_type, axis=1)

# Save processed file
df.to_csv("processed_skincare_dataset1.csv", index=False)
print("✅ Preprocessing done! Saved as processed_skincare_dataset1.csv")
