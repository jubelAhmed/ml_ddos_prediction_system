from flask import Flask, request, jsonify
import grpc
import predict_pb2
import predict_pb2_grpc

# Initialize Flask app
app = Flask(__name__)

# gRPC client setup
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
        # Return the predictions
        return predictions

# Flask route to accept JSON data and call gRPC server
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Check if 'features' are present in the request
        if 'features' not in data:
            return jsonify({"error": "JSON must contain 'features' key"}), 400
        
        # Extract features from the JSON request
        features = data['features']

        # Ensure features is a list of numbers
        if not isinstance(features, list) or not all(isinstance(x, (int, float)) for x in features):
            return jsonify({"error": "Features must be a list of numbers"}), 400

        # Call the gRPC server to get predictions
        print(features)
        print(len(features))
        predictions = grpc_predict(features)

        # Return the predictions as a JSON response
        return jsonify({"predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
