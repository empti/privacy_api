# Create a new virtualenv named "privacy_api"

# Python 3.3+
$ python -m venv privacy_api

# Python pre 3.3
$ virtualenv privacy_api
New python executable in privacy_api/bin/python
Installing setuptools, pip, wheel...done.

# Activate the virtualenv (OS X & Linux)
$ source privacy_api/bin/activate

# To run the API server
$ python3 privacy_api.py

# To run the test, use the following script
# Or you can run curl command to send request to API directly
$ test_basic.sh
