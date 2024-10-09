## ML DDoS Prediction System
This project contains two main components: a gRPC server and a Flask client. Both components communicate using gRPC and share a common .proto file using a symbolic link to ensure consistency and avoid duplication. The gRPC server provides a DDoS prediction service, and the Flask client consumes this service.


## Requirements

- Python 3.7 or higher
- `grpcio` and `grpcio-tools` for gRPC communication
- Flask for the client API

## Installation

### 1. Clone the Repository

```bash
cd mLddos_prediction_system
2. Create a Symbolic Link for the .proto File
To ensure both the gRPC server and Flask client use the same .proto file, create a symbolic link:

ln -s mLddos_prediction_system/grpc_server/protos/predict.proto mLddos_prediction_system/flask_client/protos/predict.proto
```
3. Install Dependencies
Install the required Python packages for both the gRPC server and Flask client:
```bash
# Both Grpc Server and Flask Client
pip install -r requirements.txt
```
4. Generate gRPC Stubs
Generate the gRPC stubs (predict_pb2.py and predict_pb2_grpc.py) from the .proto file in both the gRPC server and Flask client directories.

gRPC Server
```bash
cd mLddos_prediction_system/grpc_server
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/predict.proto
Flask Client
cd mLddos_prediction_system/flask_client
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/predict.proto
```
1. Run the gRPC Server
Start the gRPC server to listen for incoming prediction requests:
```bash
cd mLddos_prediction_system/grpc_server
python grpc_server.py
```
The server will run on localhost:50051 and provide prediction services.

2. Run the Flask Client
Start the Flask client that communicates with the gRPC server to request predictions:
```bash
cd mLddos_prediction_system/flask_client
python flask_client_api.py
```
The Flask client will run on localhost:5000.

3. Test the Client-Server Communication
You can use curl or Postman to send a POST request to the Flask client API to get predictions:
```bash
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"features": []}'

## Here, "features" are the input variables for the model used to predict the type of DDoS attack. 
## These features represent the transformed data necessary for the prediction process.

curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"features": [6,2,3,0,1125.0,0.0,1094.0,0.0,375.0,622.8652,0.0,0.0,0.0,0.0,20.14790169382063,14.220976332738882,0.6931471805599453,0.0,0.6931471805599453,0.6931471805599453,1.0986122886681096,0.6931471805599453,0.0,0.6931471805599453,0.6931471805599453,0.0,0.0,0.0,0.0,0.0,1,4.574710978503383,0.0,14.220976332738882,0.0,0.0,1094.0,554.75,622.80084,12.868456233797083,0,0,1,0,0,1,0,0,0.0,739.6667,375.0,0.0,3,1125,0,0,133,-1,1,32,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]}'

```
Expected Output:
The server should respond with a JSON containing the prediction results:
```bash
{
  "result": "Prediction Successful",
  "predictions": [0]
}
```

Development
Regenerate gRPC Stubs
If you make changes to the predict.proto file, you will need to regenerate the gRPC stubs:

gRPC Server:
```bash
cd mLddos_prediction_system/grpc_server
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/predict.proto
```
Flask Client:
```bash
cd mLddos_prediction_system/flask_client
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/predict.proto
```
Notes
- Ensure that the symbolic link is correctly set up. If you move the project or change directories, you may need to recreate the symlink.
- Both server and client need to have the same version of the .proto file to ensure compatibility.

#### Disclaimer
This project is an overview of using a machine learning model for DDoS attack prediction. It does not fully represent real-world use cases and should be treated as a prototype rather than a production-ready solution. For effective DDoS prediction, it is essential to integrate a Network Packet Capture Layer (such as Wireshark) and a Feature Extraction Layer. These components are crucial for capturing network traffic and extracting relevant features necessary for accurate predictions, which are not implemented in this project.