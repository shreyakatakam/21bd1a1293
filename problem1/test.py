import requests

# URL of the endpoint
url = "http://20.244.56.144/test/p"

# Send a GET request to the endpoint
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("Response received successfully!")
    print(data)
else:
    print(f"Failed to get response. Status code: {response.status_code}")
    print(response.text)
