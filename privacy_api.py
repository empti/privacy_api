#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import spacy

nlp = spacy.load("en_core_web_sm")


app = Flask(__name__)

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
    data_message = data_content['message']
    # label is not required for the demo
    # data_labels = data_content['labels']
    
    # process the data_message
    nlp_doc = nlp(data_message)
    
    # Initialize the response
    data_result = {}
    data_matchings = []
    data_match_decision = False 
    
    for entity in nlp_doc.ents:
        data_match_decision = True;
        data_matching_object = {}
        data_matching_object['type'] = entity.label_
        data_matching_object['value'] = entity.text
        data_matching_object['requirements'] = []
        # process the entity label through label -> regulation/compliance mapping
        # The following hard-coded 'CCPA' will be replaced with actual mapping
        data_matching_object['requirements'].append('CCPA')
        print (data_matching_object)

        data_matchings.append(data_matching_object)

    data_result['match'] = data_match_decision
    data_result['matchings'] = data_matchings

    return jsonify(data_result), 201

if __name__ == '__main__':
    app.run(debug=True)