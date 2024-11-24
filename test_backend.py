import requests

# URL of your Flask backend
url = "http://127.0.0.1:5000/filter"

# Data to send to the backend
data = {
    "Price_Range": "$20K-$30K",
    "Body": "Sport Utility",
    "Ext_Color_Generic": "Red"
}

# Make the POST request
response = requests.post(url, json=data)

# Print the response from the server
print("Response from the backend:")
print(response.json())
