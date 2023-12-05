import requests
import json

# Make a GET request
response = requests.get('http://VM_IP:8080/')
print("GET Response:")
print(response.text)

# Make a POST request with JSON data
data = {'command': 'ipconfig', 'arg': '/all'}
headers = {'Content-type': 'application/json'}
response = requests.post('http://localhost:8080/data', data=json.dumps(data), headers=headers)
print("\nPOST Response:")
print(response.text)