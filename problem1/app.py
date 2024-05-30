from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
WINDOW_SIZE = 10
API_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibonacci',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}
stored_numbers = []

# Function to fetch numbers from third-party API
def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"Error fetching numbers: {e}")
        return []

@app.route('/numbers/<id_type>', methods=['GET'])
def get_numbers(id_type):
    if id_type not in API_URLS:
        return jsonify({"error": "Invalid number ID type"}), 400

    global stored_numbers

    # Fetch numbers from third-party API
    numbers = fetch_numbers(API_URLS[id_type])

    # Filter out duplicates
    unique_numbers = [num for num in numbers if num not in stored_numbers]

    # Update the stored numbers
    window_prev_state = stored_numbers.copy()
    stored_numbers.extend(unique_numbers)
    stored_numbers = list(dict.fromkeys(stored_numbers))  # Ensure uniqueness

    # Limit to the window size
    if len(stored_numbers) > WINDOW_SIZE:
        stored_numbers = stored_numbers[-WINDOW_SIZE:]

    # Calculate the average
    if len(stored_numbers) > 0:
        avg = sum(stored_numbers) / len(stored_numbers)
    else:
        avg = 0.0

    return jsonify({
        "windowPrevState": window_prev_state,
        "windowCurrState": stored_numbers,
        "numbers": numbers,
        "avg": round(avg, 2)
    })

if __name__ == '__main__':
    app.run(port=9876, debug=True)
