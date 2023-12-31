from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from Texture import *
from color import *

def getColor(base64):
    rgb_array = get_rgb_array_from_image(base64)
    blocks_rgb_array = create_blocks_array(rgb_array)
    block_hsv_array = create_hsv_array_from_rgb_array(blocks_rgb_array)
    return block_hsv_array

class ImageVal:
    def __init__(self, Image:str, Val:float):
        self.Image = Image
        self.Val = Val

    def to_dict(self):
       return {
           'Image': self.Image,
           'Val': self.Val
       }

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your Flask app
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

dataset = None  # Initialize the dataset as a global variable
ref = None  # Initialize the ref variable as a global variable
def pangkasBase64(base64: str):
   # Split the string at the first comma
   split_string = base64.split(',', 1)
   
   # Return the part of the string after the first comma
   if len(split_string) > 1:
       return split_string[1].strip()
   else:
       return base64
   

@app.route('/api/receive', methods=['POST'])
def receive_strings():
    data = request.get_json()
    if "data" in data and isinstance(data["data"], list):
        # Access the 'data' key in the received JSON
        received_data = data["data"]

        global dataset
        dataset = received_data
        return jsonify({"message": "okay received", "dataset" : dataset})
    else:
        return jsonify({"error": "Invalid input format"}), 400

@app.route('/api/RefImage', methods=['POST'])
def receive_RefImage():
    data = request.get_json()
    if "Ref" and "Type" in data and isinstance(data["Ref"], str):
        # Access the 'data' key in the received JSON
        received_data = data["Ref"]
        type = data["Type"]
        global ref
        ref = pangkasBase64(received_data)
        pairData =[]
        if type == False:
            refTexture = getTexture(ref)
            for i in dataset:
                textureI = getTexture(pangkasBase64(i))
                pair = ImageVal(pangkasBase64(i),cosSim(refTexture,textureI))
                if not math.isnan(pair.Val) :
                    pair.Val = round((pair.Val*100),2)
                    pairData.append(pair.to_dict())    
        else:
            refColor = getColor(ref)
            for i in range(len(dataset)):
                ColorI = getColor(pangkasBase64(dataset[i]))
                pair = ImageVal(pangkasBase64(dataset[i]),average_cos_similarity(refColor,ColorI))
                if not math.isnan(pair.Val):
                    pair.Val = round((pair.Val*100),2)
                    pairData.append(pair.to_dict())          
        pairData = sorted(pairData, key=lambda d: d['Val'], reverse=True)
        return jsonify({"message": "Hasil", "pair_values" : pairData,"state": type})

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


