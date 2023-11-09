from app import *
import requests

dataset_json = requests.get('http://127.0.0.1:5000/api/get_dataset')
print(dataset_json)