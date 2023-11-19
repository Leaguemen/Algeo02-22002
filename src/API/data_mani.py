import requests

# Define the API endpoint URLs
api_url_dataset = 'http://localhost:5000/api/get_dataset'
api_url_ref = 'http://localhost:5000/api/get_ref'

# Function to fetch the dataset from the Flask API
def get_dataset():
    response = requests.get(api_url_dataset)
    if response.status_code == 200:
        data = response.json()
        return data.get('dataset')
    else:
        print(f"Error fetching dataset: {response.text}")
        return None

# Function to fetch the ref from the Flask API
def get_ref():
    response = requests.get(api_url_ref)
    if response.status_code == 200:
        data = response.json()
        return data.get('refImage')
    else:
        print(f"Error fetching ref: {response.text}")
        return None

if __name__ == '__main__':
    dataset = get_dataset()
    ref = get_ref()

    if dataset is not None:
        print(f"Dataset: {dataset}")

    if ref is not None:
        print(f"Ref Image: {ref}")