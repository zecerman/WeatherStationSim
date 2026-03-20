# WeatherStationSim
This repo is designed to simulate a weather station, it is primariy an exercise in software engineering, CI/CD pipelines, and API communication 

## Usage instructions
1. Initialize the flask server with
  python rest_api.py
2. Run the weather station with:
  python run.py

## Transformer API Design
- The endpoint of the transformer is a "database.csv" file, each row represents the aggregated results of a every sensor in the weather stations domain during a given timestamp
- The weather station takes user input not from the command line, but rather reads its parameters from the "config.json" file which can be edited before running. Ex input:
{
  "station": {
    "timeout": 5,
    "api_url": "http://127.0.0.1:5000/weather",
    "count": 3,
    "sensors_per_sampler": 10
  }
}
- The output of the weather station is represents the aggregated results of a every sensor in the weather stations domain during a given timestamp. In addition to being stored in a csv database, it is also served with Flask POST requests to the caller. Ex output:
Starting weather station pipeline...
Data stored: {'data': [1774034064, 122.63, 61.32]}
Data stored: {'data': [1774034069, 123.2, 61.6]}
etc...

## Test cases
In order to run node.js tests:
Setup and Run Instructions

1. Install Python dependencies

  pip install -r requirements.txt

    Installs Python packages: Flask, requests, numpy

2. Install Node.js dependencies

  npm install

    Make sure Node.js LTS is installed from nodejs.org

3. Start Node.js server

  npm start

    Starts your sampler API on http://localhost:3000/sample

4. Run Node.js unit tests

  npm test

    Verifies your sampler logic with pre-defined test data

5. Demo / end-to-end pipeline (Don't include in README but do include in Demo video)

In another terminal, run:

  python sampler.py

    This sends live simulated sensor data to the Node server automatically.

