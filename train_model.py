import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_on_real_data():
    if not os.path.exists("heart.csv"):
        print("CSV file not found.")
        return
    
    # Load dataset
    df = pd.read_csv("heart.csv")
    
    # Check for missing values
    df = df.dropna()
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Accuracy check (optional message)
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy*100:.2f}%")
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Real data model saved as model.pkl")

if __name__ == "__main__":
    train_on_real_data()
