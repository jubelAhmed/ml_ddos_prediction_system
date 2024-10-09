from flask import Flask, request, jsonify
import grpc
import predict_pb2
from generated import predict_pb2, predict_pb2_grpc

# Initialize the Flask app
app = Flask(__name__)

# Dictionary to keep track of blocked IPs
blocked_ips = set()

# Function to check if an IP is blocked
def is_blocked(ip):
    return ip in blocked_ips

# Function to communicate with gRPC server and get predictions
def grpc_predict(features):
    # Establish a channel with the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = predict_pb2_grpc.PredictionServiceStub(channel)

        # Create a request with the provided features
        request = predict_pb2.PredictRequest(features=features)

        # Make a prediction request and receive the response
        response = stub.Predict(request)

        # Convert the gRPC response to a standard Python list
        predictions = list(response.predictions)

        # Return the predictions as a Python list
        return predictions

# Flask route to accept JSON data, call gRPC server, and block IPs if an attack is detected
@app.route('/predict', methods=['POST'])
def predict_and_block():
    # Get the client IP address
    client_ip = request.remote_addr

    # Check if the IP is blocked
    if is_blocked(client_ip):
        return jsonify({"error": "Your IP has been blocked due to malicious activity."}), 403

    try:
        # Get JSON data from the request
        data = request.get_json()

        # Ensure data is provided and contains necessary keys
        if 'features' not in data:
            return jsonify({"error": "JSON must contain 'features' key with input data"}), 400

        # Extract features from the JSON request
        features = data['features']

        # Ensure features is a list of numbers
        if not isinstance(features, list) or not all(isinstance(x, (int, float)) for x in features):
            return jsonify({"error": "Features must be a list of numbers"}), 400

        # Call the gRPC server to get predictions
        predictions = grpc_predict(features)

        # Check if the prediction is an attack
        if 1 in predictions:  # Assuming 1 indicates an attack
            blocked_ips.add(client_ip)  # Block the client's IP
            return jsonify({"result": "Attack detected! Your IP has been blocked."}), 403

        # If the prediction is benign
        return jsonify({"result": "Normal", "predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
