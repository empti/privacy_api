#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import pandas as pd
import re
import spacy

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

privacy_type_mapping_filename = 'privacy_type_mapping.csv'
privacy_type_mapping = pd.read_csv(
    privacy_type_mapping_filename,
    index_col=0,
    keep_default_na=False,
    converters={"Requirements": lambda x: x.split("\n") if x else None},
).to_dict('index')


def extract_email(text):
    return re.findall('[A-Za-z0-9]+[A-Za-z0-9._%+-]*@\w+.\w{2,4}', text)


def extract_phone(text):
    return re.findall('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)


def extract_chd(text):
    return re.findall('[0-9]{16}', text)

# The API endpoint is: /data/api/v0.1/classify

@app.route('/data/api/v0.1/classify', methods=['GET'])
def get_sample():
    return jsonify(samples[0])


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Format not allowed'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/data/api/v0.1/classify', methods=['POST'])
def process_data():
    # if not request.json or not 'title' in request.json:
    if not request.json:
        abort(400)
    data_content = request.get_json(silent=False)
    if 'message' in data_content:
        data_message = data_content['message']
    else:
        raise ValueError("Invalid input, 'message' not exist!")

    # label is not required for the demo
    # data_labels = data_content['labels']
    
    # process the data_message
    nlp_doc = nlp(data_message)
    
    # Initialize the response
    data_matchings = []
    
    for entity in nlp_doc.ents:
        if entity.label_ in privacy_type_mapping and privacy_type_mapping[entity.label_]['Requirements']:
            data_matching_object = {
                'type': entity.label_,
                'value': entity.text,
                'requirements': privacy_type_mapping[entity.label_]['Requirements'],
            }
            data_matchings.append(data_matching_object)

    for extracted in extract_email(nlp_doc.text) + extract_phone(nlp_doc.text):
        data_matching_object = {
            'type': 'CONTACT',
            'value': extracted,
            'requirements': ['GLBA', 'CCPA', 'PIPEDA'],
        }
        data_matchings.append(data_matching_object)

    for extracted in extract_chd(nlp_doc.text):
        data_matching_object = {
            'type': 'CHD',
            'value': extracted,
            'requirements': ['PCI'],
        }
        data_matchings.append(data_matching_object)

    data_result = {
        'match': bool(data_matchings),
        'matchings': data_matchings,
    }

    return jsonify(data_result), 201


if __name__ == '__main__':
    app.run(debug=True)
