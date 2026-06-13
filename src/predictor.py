import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "flood_predictor.joblib")

def train_model(data_path="data/regional_data.csv"):
    """
    Loads data, trains a Random Forest Classifier, and saves the model.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}. Run data generator first.")
        
    df = pd.read_csv(data_path)
    
    # Define Features (X) and Target (y)
    X = df[["elevation_meters", "rainfall_mm", "population_density", "bridge_count"]]
    y = df["historical_flooded"]
    
    # Split into 80% training and 20% testing data (FIXED ARGUMENT HERE)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate accuracy to verify it works well
    accuracy = model.score(X_test, y_test)
    print(f"Model trained successfully. Test Accuracy: {accuracy * 100:.2f}%")
    
    # Ensure models directory exists and save the trained model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved securely to {MODEL_PATH}")
    return model

def predict_flood_risk(elevation, rainfall, pop_density, bridge_count):
    """
    Loads the trained model and returns the risk probability (0.0 to 1.0) for a sector.
    """
    if not os.path.exists(MODEL_PATH):
        print("Model file not found. Running training script first...")
        train_model()
        
    model = joblib.load(MODEL_PATH)
    
    # Format the input features exactly how the model expects them
    input_data = pd.DataFrame([[elevation, rainfall, pop_density, bridge_count]], 
                               columns=["elevation_meters", "rainfall_mm", "population_density", "bridge_count"])
    
    # predict_proba returns [prob_of_0, prob_of_1]. We want prob_of_1 (flooding risk)
    risk_probability = model.predict_proba(input_data)[0][1]
    return float(risk_probability)

if __name__ == "__main__":
    # Test execution
    train_model()
    # Test a prediction case (Low elevation, massive rainfall, high risk)
    sample_risk = predict_flood_risk(elevation=12.5, rainfall=380.0, pop_density=3500, bridge_count=3)
    print(f"Sample Sector Risk Assessment: {sample_risk * 100:.1f}% chance of flooding.")