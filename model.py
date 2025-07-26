import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split   
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# Importing the dataset
df = pd.read_csv('Data/tic-tac-toe.csv')

# Count for missing values
missing_values_count = df.isnull().sum()
print("Missing values count in each column:")
print(missing_values_count)

# Display the first few rows of the dataset
print(df.head())

# Convert to numerical values
for col in df.columns[:-1]:  # Exclude the last column (target)
    df[col] = df[col].map({'x': 1, 'o': -1, 'b': 0})
df['class'] = df['class'].map({'positive': 1, 'negative': -1})

# Check for missing values after mapping
if df.isnull().values.any():
    print("Warning: Missing values detected after mapping!")
    print(df.isnull().sum())
    print("Rows with missing values will be dropped.")
    df.dropna(inplace=True)

# Prepare features and target
X = df.iloc[:, :-1].values # Features (all columns except the last)
y = df.iloc[:, -1].values # Target (last column ONLY )

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Decision Tree Classifier
model = DecisionTreeClassifier(max_leaf_nodes=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Plot the tree (first 9 levels for readability)
plt.figure(figsize=(20, 10))
plot_tree(
    model, 
    feature_names=df.columns[:-1],  # Fix: use actual column names for features
    class_names=["negative", "positive"], 
    filled=True, 
    max_depth=9
)
plt.title("Decision Tree for Tic Tac Toe Endgame")
plt.show()

#save the model
import joblib
joblib.dump(model, 'tic_tac_toe_decision_tree.joblib')