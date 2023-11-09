from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module


app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your Flask app
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

dataset = None  # Initialize the dataset as a global variable
ref = None  # Initialize the ref variable as a global variable

@app.route('/api/receive', methods=['POST'])
def receive_strings():
    data = request.get_json()
    if "data" in data and isinstance(data["data"], list):
        # Access the 'data' key in the received JSON
        received_data = data["data"]

        global dataset
        # Manipulate the data (for example, you can reverse the list)
        dataset = received_data
        return jsonify({"message": "okay received", "dataset" : dataset})
    else:
        return jsonify({"error": "Invalid input format"}), 400

@app.route('/api/RefImage', methods=['POST'])
def receive_RefImage():
    data = request.get_json()
    if "Ref" in data and isinstance(data["Ref"], str):
        # Access the 'data' key in the received JSON
        received_data = data["Ref"]
        global ref
        ref = received_data
        return jsonify({"message": "okay received", "refImage" : ref})
    else:
        return jsonify({"error": "Invalid input format"}), 400

@app.route('/api/get_dataset', methods=['GET'])
def get_dataset():
    global dataset
    return jsonify({"dataset": dataset})

@app.route('/api/get_ref', methods=['GET'])
def get_ref():
    global ref
    return jsonify({"refImage": ref})


if __name__ == '__main__':
    app.run(debug=True)

