import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split   
from sklearn.tree import  plot_tree
from sklearn.ensemble import RandomForestClassifier
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#random forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validated accuracy: {scores.mean():.2%}")

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 6, 8, 10],
    'min_samples_split': [2, 4, 6],
    'min_samples_leaf': [1, 2, 4]
}
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
grid_search.fit(X, y)
print("Best parameters:", grid_search.best_params_)
print("Best cross-validated accuracy:", grid_search.best_score_)

# # Plot the random forest trees (first 5 trees for readability)
# for idx, tree in enumerate(model.estimators_[:5]):
#      plt.figure(figsize=(20, 10))
#      plot_tree(
#           tree, 
#           feature_names=df.columns[:-1],  # Fix: use actual column names for features
#           class_names=["negative", "positive"], 
#           filled=True, 
#           max_depth=9
#      )
#      plt.title(f"Decision Tree {idx + 1} for Tic Tac Toe Endgame")
#      plt.show()
# import math

# n_trees = len(model.estimators_)
# cols = 10  # Number of columns in the grid
# rows = math.ceil(n_trees / cols)

# fig, axes = plt.subplots(rows, cols, figsize=(cols*2, rows*2))
# axes = axes.flatten()

# for idx, tree in enumerate(model.estimators_):
#     plot_tree(
#         tree,
#         feature_names=df.columns[:-1],
#         class_names=["negative", "positive"],
#         filled=True,
#         max_depth=2,  # Make each tree mini (show only top 2 levels)
#         ax=axes[idx]
#     )
#     axes[idx].set_title(f"Tree {idx+1}", fontsize=8)
#     axes[idx].axis('off')  # Hide axes for clarity

# # Hide any unused subplots
# for ax in axes[n_trees:]:
#     ax.axis('off')

# plt.tight_layout()
# plt.suptitle("All Random Forest Trees (Mini, Top 2 Levels)", fontsize=16, y=1.02)
# plt.show()


#save the model
import joblib
joblib.dump(model, 'tic_tac_toe_random_forest.joblib')