# This program simulates the operation of a weather station's rest_api.
# It fascilitates communication between the stations central transformer and its database(s)

import csv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_FILE_PATH = 'database.csv'

# Handle the edge case that the database does not yet exist
def initialize_database():
    if not os.path.exists(DATABASE_FILE_PATH):
        with open(DATABASE_FILE_PATH, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['timestamp', 'voltage', 'temperature', 'precipitation'])

# Flask hook
@app.route('/weather', methods=['POST'])
def write_weather_data():
    data = request.get_json()
    # Handle no/bad data
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    # Else, append data as row
    with open(DATABASE_FILE_PATH, 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            data['timestamp'],
            data['voltage'],
            data['temperature'],
            data['precipitation']
        ])
    # Communicate success via terminal
    return jsonify({'message': 'Weather data stored successfully'}), 201

if __name__ == '__main__':
    initialize_database()
    app.run(host='127.0.0.1', port=5000, debug=True)