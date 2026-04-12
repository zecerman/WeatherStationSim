# This program simulates the operation of a weather station's rest_api.
# It fascilitates communication between the stations central transformer and its database(s)

import os
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


conn = psycopg2.connect(
     host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "weatherdb"),
    user=os.getenv("DB_USER", "weatheruser"),
    password=os.getenv("DB_PASSWORD", "weatherpass")
)

cur = conn.cursor()

# Flask hook
@app.route('/weather', methods=['POST'])
def write_weather_data():
    data = request.get_json()
    # Handle no/bad data
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    if not all(k in data for k in ('timestamp', 'voltage', 'temperature')):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        # Insert into database
        cur.execute(
            """
            INSERT INTO weather_data (timestamp, voltage, temperature)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (data['timestamp'], data['voltage'], data['temperature'])
        )

        record_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({
            'status': 'stored',
            'id': record_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)