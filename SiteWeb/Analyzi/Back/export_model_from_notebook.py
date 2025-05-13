"""
This script shows how to properly export a model from a Jupyter notebook
to be used in a Flask application.
"""

import joblib
import pickle
import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def export_model_from_notebook(model, output_path):
    """
    Export a model from a notebook to a format that can be loaded by Flask.
    
    Args:
        model: The trained model object
        output_path: Path to save the exported model
    """
    print(f"Exporting model to {output_path}")
    
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the model with joblib (more reliable for Flask)
        joblib.dump(model, output_path)
        print(f"Model successfully exported to {output_path}")
        
        return True
    
    except Exception as e:
        print(f"Error exporting model: {e}")
        return False

# Example usage - this would be in your notebook
if __name__ == "__main__":
    # This is just a dummy model for demonstration
    # In your notebook, you would use your actual trained model
    dummy_model = RandomForestClassifier(n_estimators=10)
    dummy_model.fit(
        np.random.rand(100, 20),  # Random features
        np.random.choice([0, 1, 2], size=100)  # Random labels
    )
    
    # Export the model
    export_model_from_notebook(
        dummy_model, 
        'models/electrical-motor-fault-analysis-with-motor-fae75b.pkl'
    )
