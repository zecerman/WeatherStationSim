# WeatherStationSim
This repo is designed to simulate a weather station, it is primariy an exercise in software engineering, CI/CD pipelines, and API communication 


    To run the program you must:
Have all files in the same directory including the following db file and headers
    database.csv
    timestamp,voltage,temperature,precipitation
Initialize the flask server with
    python rest_api.py
Run the transformer with:
    python transformer.py










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

