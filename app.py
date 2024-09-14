from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load scaler and model from .pkl files
scaler_filename = 'StandardScaler_scaler.pkl'  # Replace with your scaler filename
model_filename = 'StandardScaler_SGDClassifier_model.pkl'  # Replace with your model filename

with open(scaler_filename, 'rb') as file:
    scaler = pickle.load(file)

with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Define a route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()
    
    # Convert the data into a DataFrame for easier processing
    df = pd.DataFrame(data)
    
    # Check if required columns are present
    required_columns = [
        'protocol', 'flow_duration', 'total_fwd_packets', 'total_backward_packets',
        'total_length_of_fwd_packets', 'total_length_of_bwd_packets', 'fwd_packet_length_max',
        'fwd_packet_length_min', 'fwd_packet_length_mean', 'fwd_packet_length_std',
        'bwd_packet_length_max', 'bwd_packet_length_min', 'bwd_packet_length_mean',
        'bwd_packet_length_std', 'flow_bytes_s', 'flow_packets_s', 'flow_iat_mean',
        'flow_iat_std', 'flow_iat_max', 'flow_iat_min'
    ]
    
    if not all(column in df.columns for column in required_columns):
        return jsonify({"error": "Some required columns are missing in the input data"}), 400
    
    # Select only the required columns and apply the scaler
    input_data = df[required_columns]
    input_data_scaled = scaler.transform(input_data)

    # Make prediction using the loaded model
    predictions = model.predict(input_data_scaled)
    
    # Convert predictions to a list
    predictions_list = predictions.tolist()
    
    # Return the predictions as a JSON response
    return jsonify({"predictions": predictions_list})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
