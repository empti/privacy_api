# A***** Privacy API

### Requires Python 3.3+

## Create a new virtualenv named ".env" and activate it

$ python3 -m venv .env

$ virtualenv .env

$ source .env/bin/activate

## Run the setup.sh to install dependencies

$ chmod u+x setup.sh

$ ./setup.sh

## To run the API server
$ python3 privacy_api.py

## To run the dmeo
$ streamlit run demo.py 

## To run the test, use the following script

$ chmod u+x test_basic.sh

$ test_basic.sh

## The test data (request body) is in the following file:
$ body.json
