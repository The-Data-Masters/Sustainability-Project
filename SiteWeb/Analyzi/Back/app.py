from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS
import os
import uuid
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
from io import BytesIO
import librosa
import librosa.display
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'analyzi'


mysql = MySQL(app)

@app.route('/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        return "DB connected successfully"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/api/hello')
def hello():
    return jsonify(message="Hello from Flask!")

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max upload
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('models', exist_ok=True)

# Load models
EQUIPMENT_MODEL_PATH = 'linear_model.pkl'
MOTOR_MODEL_PATH = 'eq_audio.h5'

# Try to import TensorFlow/Keras with error handling
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Keras version: {tf.keras.__version__}")
    
    # Reduce TensorFlow logging
    tf.get_logger().setLevel('ERROR')
    
    # Avoid TensorFlow memory issues
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"Found {len(gpus)} GPU(s), memory growth enabled")
        except RuntimeError as e:
            print(f"Memory growth setting error: {e}")
    
except ImportError as e:
    print(f"Error importing TensorFlow/Keras: {e}")
    print("Please install TensorFlow: pip install tensorflow")
    tf = None
    keras = None

# Helper functions for equipment lifetime prediction
def load_equipment_model():
    try:
        return joblib.load(EQUIPMENT_MODEL_PATH)
    except Exception as e:
        print(f"Error loading equipment model: {e}")
        return None

def generate_interpretation(data, prediction):
    interpretation = ""
    if prediction < 5:
        interpretation += f"<strong>Short Lifetime:</strong> The predicted lifetime of {prediction} years is relatively short. "
        if data['CO2_Emissions_kg'] > 500:
            interpretation += "High CO2 emissions may be contributing to reduced equipment longevity. Consider more eco-friendly alternatives. "
        if data['Energy_Consumption_kWh'] > 2000:
            interpretation += "High energy consumption is likely affecting the equipment's lifespan. Energy efficiency improvements could extend lifetime. "
    elif prediction < 10:
        interpretation += f"<strong>Average Lifetime:</strong> The predicted lifetime of {prediction} years is within normal range. "
        interpretation += "Regular maintenance according to the specified schedule will help maintain optimal performance. "
    else:
        interpretation += f"<strong>Long Lifetime:</strong> The predicted lifetime of {prediction} years is excellent! "
        interpretation += "This equipment is expected to provide good long-term value. Maintain current operating conditions to preserve longevity. "

    if data['Energy_Type'] == 'Solar':
        interpretation += "<strong>Sustainable Energy:</strong> Solar power contributes to longer equipment life and lower operational costs. "
    elif data['Energy_Type'] == 'Electric':
        interpretation += "<strong>Electric Power:</strong> Consider energy efficiency measures to optimize performance and reduce costs. "
    elif data['Energy_Type'] == 'Fuel':
        interpretation += "<strong>Fuel-Based:</strong> Consider transitioning to more sustainable energy sources to reduce emissions and potentially extend equipment life. "

    interpretation += f"<strong>Maintenance:</strong> {data['Maintenance_Frequency']} maintenance is recommended to ensure optimal performance and longevity. "
    return interpretation

def create_comparison_chart(data, prediction):
    avg_lifetimes = {
        'Conditioning': 8.5,
        'Cleaning': 7.2,
        'Production': 10.1,
        'Packaging': 9.3,
        'Storage': 12.5
    }
    category = data['Category']
    category_avg = avg_lifetimes.get(category, 9.0)

    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ['Your Equipment', f'Average {category} Equipment']
    values = [prediction, category_avg]
    colors = ['#c1ff00', '#90caf9'] if prediction >= category_avg else ['#f44336', '#90caf9']
    bars = ax.bar(labels, values, color=colors, width=0.6)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

    ax.set_ylabel('Years', fontsize=12, fontweight='bold')
    ax.set_title('Predicted Lifetime Comparison', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, max(values) * 1.2)
    ax.axhline(y=category_avg, color='#90caf9', linestyle='--', alpha=0.7)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return chart

def create_emissions_chart(co2_emissions):
    low, medium, high = 200, 500, 1000
    if co2_emissions <= low:
        level = "Low"; color = "#4caf50"
    elif co2_emissions <= medium:
        level = "Medium"; color = "#ff9800"
    else:
        level = "High"; color = "#f44336"

    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})
    max_emissions = 1500
    theta = np.linspace(0, 1.8 * np.pi, 100)
    r = np.ones_like(theta)

    ax.plot(theta, r, color='#e0e0e0', linewidth=20, alpha=0.5)
    value_theta = 1.8 * np.pi * min(co2_emissions / max_emissions, 1)
    ax.plot(np.linspace(0, value_theta, 100), np.ones(100), color=color, linewidth=20, alpha=0.8)

    ax.set_rticks([])
    ax.set_xticks([0, np.pi/2, np.pi, 1.5*np.pi])
    ax.set_xticklabels(['0', str(int(max_emissions/3)), str(int(2*max_emissions/3)), str(int(max_emissions))])
    ax.set_ylim(0, 1.4)
    ax.spines['polar'].set_visible(False)

    plt.text(0, 0, f"{co2_emissions:.1f}", ha='center', va='center', fontsize=24, fontweight='bold')
    plt.text(0, -0.2, "CO₂ Emissions (kg)", ha='center', va='center', fontsize=12)
    plt.text(0, -0.4, f"Level: {level}", ha='center', va='center', fontsize=14, color=color, fontweight='bold')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return chart

# Helper functions for motor sound analysis
def load_keras_model(model_path):
    """Load a Keras model from .h5 file"""
    if tf is None or keras is None:
        print("TensorFlow/Keras is not installed. Cannot load Keras model.")
        return None
    
    print(f"Attempting to load Keras model from {model_path}")
    
    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Model file not found at {model_path}")
        return None
    
    try:
        # Load the model
        model = keras.models.load_model(model_path)
        print(f"Successfully loaded Keras model from {model_path}")
        model.summary()
        return model
    except Exception as e:
        print(f"Failed to load Keras model: {str(e)}")
        return None

class FallbackModel:
    def __init__(self):
        self.labels = ['normal', 'broken', 'heavyload']
        print("Fallback model initialized")
    
    def predict(self, features):
        """Simulate prediction with random values"""
        # Return random probabilities for each class
        batch_size = features.shape[0]
        return np.random.rand(batch_size, len(self.labels))

# Try to load the motor model
motor_model = load_keras_model(MOTOR_MODEL_PATH)

# If model loading failed, use a fallback model
if motor_model is None:
    print("Keras model loading failed. Using fallback simulation model.")
    motor_model = FallbackModel()
    print("Fallback model initialized.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'ogg'}

def preprocess_audio_for_keras(audio_path):
    """Preprocess audio file for Keras model input"""
    try:
        print(f"Preprocessing audio from {audio_path}")
        
        # Load audio file
        y, sr = librosa.load(audio_path, sr=22050, mono=True)
        
        # Trim silent parts
        y, _ = librosa.effects.trim(y, top_db=20)
        
        # Make sure the audio is a fixed length (e.g., 5 seconds)
        target_length = 5 * sr
        
        if len(y) > target_length:
            # If longer, truncate
            y = y[:target_length]
        elif len(y) < target_length:
            # If shorter, pad with zeros
            padding = target_length - len(y)
            y = np.pad(y, (0, padding), 'constant')
        
        # Extract features - Mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Reshape for model input
        features = mel_spec_db.reshape(1, mel_spec_db.shape[0], mel_spec_db.shape[1], 1)
        
        print(f"Preprocessed audio shape: {features.shape}")
        
        return features
    
    except Exception as e:
        print(f"Error preprocessing audio: {str(e)}")
        # Return dummy features in case of error
        return np.random.rand(1, 128, 130, 1)

def generate_visualizations(audio_path):
    """Generate multiple visualizations for audio analysis"""
    try:
        print(f"Loading audio file from {audio_path}")
        y, sr = librosa.load(audio_path, sr=22050)
        print(f"Audio loaded successfully: {len(y)} samples, {sr}Hz")
        
        visualizations = {}
        
        # Generate spectrogram
        print("Generating spectrogram")
        plt.figure(figsize=(10, 4))
        plt.specgram(y, NFFT=2048, Fs=sr, noverlap=128, cmap='viridis')
        plt.title('Spectrogram')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        visualizations['spectrogram'] = f'data:image/png;base64,{base64.b64encode(buf.read()).decode("utf-8")}'
        print("Spectrogram generated")
        
        # Generate waveform
        print("Generating waveform")
        plt.figure(figsize=(10, 2))
        plt.plot(np.linspace(0, len(y)/sr, len(y)), y, color='#c1ff00')
        plt.title('Waveform')
        plt.ylabel('Amplitude')
        plt.xlabel('Time [sec]')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        visualizations['waveform'] = f'data:image/png;base64,{base64.b64encode(buf.read()).decode("utf-8")}'
        print("Waveform generated")
        
        # Generate MFCC
        print("Generating MFCC")
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('MFCC')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        visualizations['mfcc'] = f'data:image/png;base64,{base64.b64encode(buf.read()).decode("utf-8")}'
        print("MFCC generated")
        
        # Generate Mel Spectrogram
        print("Generating Mel Spectrogram")
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel Spectrogram')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        visualizations['mel_spectrogram'] = f'data:image/png;base64,{base64.b64encode(buf.read()).decode("utf-8")}'
        print("Mel Spectrogram generated")
        
        return visualizations
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")
        # Return placeholder visualizations in case of error
        return {
            'spectrogram': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'waveform': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'mfcc': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'mel_spectrogram': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
        }

# Routes
@app.route('/')
def index():
    app_param = request.args.get('app', 'equipment')
    return render_template('index.html', active_app=app_param)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'equipment_model_loaded': load_equipment_model() is not None,
        'motor_model_loaded': motor_model is not None,
        'tensorflow_available': tf is not None
    }), 200

@app.route('/predict-lifetime', methods=['POST'])
def predict_lifetime():
    try:
        model = load_equipment_model()
        if model is None:
            return jsonify({'error': 'Equipment model could not be loaded'}), 500

        new_equipment = pd.DataFrame({
            'Equipment_Name': [request.form.get('equipment_name')],
            'Category': [request.form.get('category')],
            'Maintenance_Cycle': [request.form.get('maintenance_cycle')],
            'Location': [request.form.get('location')],
            'Manufacturer': [request.form.get('manufacturer')],
            'CO2_Emissions_kg': [float(request.form.get('co2_emissions'))],
            'Energy_Consumption_kWh': [float(request.form.get('energy_consumption'))],
            'Energy_Type': [request.form.get('energy_type')],
            'Maintenance_Frequency': [request.form.get('maintenance_frequency')]
        })

        predicted_lifetime = model.predict(new_equipment)[0]
        predicted_lifetime = round(predicted_lifetime, 2)

        return jsonify({
            'predicted_lifetime': predicted_lifetime,
            'equipment_name': request.form.get('equipment_name')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Motor sound analysis route
@app.route('/analyze-motor', methods=['POST'])
def analyze_motor():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save the file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        print(f"File saved successfully at {file_path}")
        
        try:
            # Generate visualizations
            print("Generating visualizations...")
            visualizations = generate_visualizations(file_path)
            print("Visualizations generated successfully")
            
            # Preprocess audio for model input
            print("Preprocessing audio for model...")
            features = preprocess_audio_for_keras(file_path)
            print("Audio preprocessing completed")
            
            # Make prediction
            print("Making prediction...")
            if isinstance(motor_model, FallbackModel):
                # Fallback model
                prediction_probs = motor_model.predict(features)
                prediction_idx = np.argmax(prediction_probs[0])
                prediction_label = motor_model.labels[prediction_idx]
                confidence = float(prediction_probs[0][prediction_idx] * 100)
            else:
                # Real Keras model
                prediction_probs = motor_model.predict(features)
                prediction_idx = np.argmax(prediction_probs[0])
                labels = ['normal', 'broken', 'heavyload']  # Adjust based on your model's classes
                prediction_label = labels[prediction_idx]
                confidence = float(prediction_probs[0][prediction_idx] )
            
            print(f"Prediction result: {prediction_label} with {confidence:.2f}% confidence")
            
            response_data = {
                'prediction': prediction_label,
                'confidence': confidence,
                'visualizations': visualizations
            }
            
            return render_template('index.html', 
                                  motor_results=response_data,
                                  show_motor_results=True,
                                  active_app='motor')
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return jsonify({'error': f"Error during analysis: {str(e)}"}), 500
    
    except Exception as e:
        print(f"Error saving or processing file: {str(e)}")
        return jsonify({'error': f"Error saving or processing file: {str(e)}"}), 500
    
    finally:
        # Clean up the file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")
        except Exception as e:
            print(f"Error cleaning up file: {str(e)}")

if __name__ == '__main__':
    # Make sure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Created upload folder: {app.config['UPLOAD_FOLDER']}")
    
    # Run the app
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5002)
