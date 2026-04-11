# WeatherStationSim
This repo is designed to simulate a weather station, it is primariy an exercise in software engineering, CI/CD pipelines, and API communication 

## Usage instructions
1. Initialize the flask server with
  python rest_api.py
2. Run the weather station with:
  python run.py

## REST API Design
### Endpoint definition
- The REST API has the endpoint hook: @app.route('/weather', methods=['POST'])
### Input JSON example
- The weather station relies on user input to specify its configuration. It reads its parameters from the "config.json" file which can be edited before running. 
{
  "station": {
    "timeout": 5,
    "api_url": "http://127.0.0.1:5000/weather",
    "count": 3,
    "sensors_per_sampler": 10
  }
}
### Output JSON example
- The output of the weather station is represents the aggregated results of a every sensor in the weather stations domain during a given timestamp. It is served with Flask POST requests to the caller. Example terminal output during running:
Starting weather station pipeline...
Data stored: {'data': [1774034064, 122.63, 61.32]}
Data stored: {'data': [1774034069, 123.2, 61.6]}
etc...
- In addition, the results are stored to a .csv file ("database.csv" by default) so that the data may be accessed at a later time (this is useful since the respnses from the POST requests are only available in real time.)

### Short explaination of the design
- The weather transformer ultimately populates a .csv file ("database.csv" by default) in which each row represents the data gathered by the entire weather station during each time stamp. This data is aggregated in two many to one relationships as follows: Sensor->Sampler/Cluster->Transformer. There are many sensors in each sampler, and there are many samplers associated with a single monolithic transformer. The design is modular such that the number of sensors in a given sampler may increase or decrease with only a quick manual edit to the JSON config input file. The same is true for the number of samplers which in the transformer's list. Because of this design, the failure of any one component (with the exception of the single transformer object) is not fatal to the function of the weather station.

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

