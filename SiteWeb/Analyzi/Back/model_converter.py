"""
This script converts a model from a Jupyter notebook format to a format
that can be loaded by Flask. Run this script to convert your model.
"""

import joblib
import pickle
import os
import sys

def convert_model(input_path, output_path):
    """
    Convert a model from a notebook format to a Flask-compatible format.
    
    Args:
        input_path: Path to the input model file
        output_path: Path to save the converted model
    """
    print(f"Converting model from {input_path} to {output_path}")
    
    try:
        # Try to load the model with different methods
        model = None
        
        # Method 1: Try joblib
        try:
            print("Trying to load with joblib...")
            model = joblib.load(input_path)
            print("Successfully loaded with joblib!")
        except Exception as e:
            print(f"Joblib loading failed: {e}")
        
        # Method 2: Try pickle
        if model is None:
            try:
                print("Trying to load with pickle...")
                with open(input_path, 'rb') as f:
                    model = pickle.load(f)
                print("Successfully loaded with pickle!")
            except Exception as e:
                print(f"Pickle loading failed: {e}")
        
        # If model is still None, we couldn't load it
        if model is None:
            print("Failed to load the model with any method.")
            return False
        
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the model with joblib (more reliable for Flask)
        print(f"Saving model to {output_path}")
        joblib.dump(model, output_path)
        print("Model successfully converted and saved!")
        
        return True
    
    except Exception as e:
        print(f"Error converting model: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python model_converter.py <input_model_path> <output_model_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    success = convert_model(input_path, output_path)
    
    if success:
        print("Model conversion completed successfully!")
    else:
        print("Model conversion failed.")
