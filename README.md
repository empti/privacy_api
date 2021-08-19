# A***** Data Privacy API

### Requires Python 3.3+

## (Recommended) Run the application in a Docker container:

$ docker build -t dpapi:v0.10 .

$ docker container run -dp 8501:8501 dpapi:v0.10

(Open a browser and use URL http://localhost:8501) 

## Create a new virtualenv named ".env" and activate it

$ python3 -m venv .env

$ virtualenv .env

$ source .env/bin/activate

## Run the setup.sh to install dependencies

$ chmod u+x setup.sh

$ ./setup.sh

## To run the API server
$ python3 privacy_api.py

## To run the demo
$ streamlit run demo.py 

Use browser to open http://localhost:8501

## To run the test, use the following script

$ chmod u+x test_basic.sh

$ test_basic.sh

## The test data (request body) is in the following file:
$ examples/body.json

## To generate more test data

$ python generate_message.py 

$ python generate_message.py test.json --person True --phone True

Generated data file is saved into example/ directory.

## To run the api on test data
$ curl -i -H "Content-Type: application/json" -X POST --data @examples/test.json http://127.0.0.1:5000/data/api/v0.1/classify
