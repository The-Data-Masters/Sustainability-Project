"""
This script shows how to properly export a Keras model from a Jupyter notebook
to be used in a Flask application.
"""

import os
import numpy as np

# Import TensorFlow with error handling
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Keras version: {tf.keras.__version__}")
except ImportError:
    print("TensorFlow not installed. Please install with: pip install tensorflow")
    exit(1)

def export_keras_model(model, output_path):
    """
    Export a Keras model to .h5 format for use in Flask.
    
    Args:
        model: The trained Keras model
        output_path: Path to save the exported model (.h5 file)
    """
    print(f"Exporting Keras model to {output_path}")
    
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the model in .h5 format
        model.save(output_path)
        print(f"Model successfully exported to {output_path}")
        
        # Test loading the model to verify it works
        test_model = keras.models.load_model(output_path)
        print("Model successfully loaded for verification")
        
        return True
    
    except Exception as e:
        print(f"Error exporting model: {e}")
        return False

# Example usage - this would be in your notebook
if __name__ == "__main__":
    # This is just a dummy model for demonstration
    # In your notebook, you would use your actual trained model
    
    # Create a simple CNN model for audio classification
    input_shape = (128, 130, 1)  # Mel spectrogram shape (adjust based on your preprocessing)
    num_classes = 3  # normal, broken, heavyload
    
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    model.summary()
    
    # Create some dummy data and train the model briefly
    X_train = np.random.random((100, *input_shape))
    y_train = np.random.randint(0, num_classes, 100)
    
    model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=1)
    
    # Export the model
    export_keras_model(
        model, 
        'models/electrical-motor-fault-analysis-with-motor-fae75b.h5'
    )
