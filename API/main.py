from flask import Flask, request , jsonify
from flask_cors import CORS

imageSet =[]
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
@app.route('/process_array', methods=['POST'])
def process_array():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Invalid JSON data"}), 400

    try:
        data = request.get_json()

        # Ensure that the JSON data is an array of strings
        if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
            return jsonify({"error": "Invalid data format. Expected an array of strings."}), 400

        # Process the array
        processed_data = [item.upper() for item in data]

        return jsonify({"result": processed_data})
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
