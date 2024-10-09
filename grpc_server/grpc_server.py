from concurrent import futures
import grpc
import pickle
import pandas as pd
import numpy as np

from generated import predict_pb2, predict_pb2_grpc


# Load scaler and model from .pkl files
scaler_filename = 'models/StandardScaler_scaler.pkl'  # Replace with your scaler filename
model_filename = 'models/StandardScaler_SGDClassifier_model.pkl'  # Replace with your model filename

with open(scaler_filename, 'rb') as file:
    scaler = pickle.load(file)

with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Implement the gRPC service
class PredictionService(predict_pb2_grpc.PredictionServiceServicer):

    def Predict(self, request, context):
        # Extract features from the request
        features = request.features
        
        # Convert the features into a 2D array (a list of lists)
        input_data = np.array([features])

        try:
            # Transform the input data using the loaded scaler
            input_data_scaled = scaler.transform(input_data)

            # Make predictions using the loaded model
            predictions = model.predict(input_data_scaled)

            # Ensure predictions are in int format (0 or 1)
            predictions_list = [int(prediction) for prediction in predictions]

            # Return the response with predictions
            return predict_pb2.PredictResponse(predictions=predictions_list)
        
        except Exception as e:
            # Log the exception and return an error
            context.set_details(f"Error processing request: {e}")
            context.set_code(grpc.StatusCode.UNKNOWN)
            return predict_pb2.PredictResponse(predictions=[])

# Set up the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    predict_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
