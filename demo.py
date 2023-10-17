import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import spacy
from spacy import displacy
from annotated_text import annotated_text
import re

colors = ['#ACDDDE',
          '#CAF1DE',
          '#E1F8DC',
          '#FEF8DD',
          '#FFE7C7',
          '#F7D8BA',
          '#C63636',
          '#FFD9A5',
          '#93AF72',
          ]

nlp = spacy.load("en_core_web_sm")

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
    return re.findall('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                      text)


def extract_chd(text):
    return re.findall('[0-9]{16}', text)


def detect(t):
    nlp_doc = nlp(t)
    data_matchings = []
    for entity in nlp_doc.ents:
        if entity.label_ in privacy_type_mapping and privacy_type_mapping[entity.label_]['Requirements']:
            data_matching_object = {
                'type': entity.label_,
                'value': entity.text,
                'requirements': privacy_type_mapping[entity.label_]['Requirements'],
            }
            data_matchings.append(data_matching_object)
            print(data_matching_object)

    for extracted in extract_email(nlp_doc.text) + extract_phone(nlp_doc.text):
        data_matching_object = {
            'type': 'CONTACT',
            'value': extracted,
            'requirements': ['GLBA', 'CCPA', 'PIPEDA'],
        }
        data_matchings.append(data_matching_object)
        print(data_matching_object)

    for extracted in extract_chd(nlp_doc.text):
        data_matching_object = {
            'type': 'CHD',
            'value': extracted,
            'requirements': ['PCI'],
        }
        data_matchings.append(data_matching_object)
        print(data_matching_object)

    data_result = {
        'match': bool(data_matchings),
        'matchings': data_matchings,
    }
    return data_matchings


def allindices(string, sub, offset=0):
    listindex = []
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)

    res = [(l, l + len(sub)) for l in listindex]
    return res

def include_all(l):
    return "(" + ", ".join(l) + ")"


image = Image.open('./Voyager_logo.png')

height, width = image.size
new_height = 600
new_width = new_height * width / height

image.thumbnail((new_width, new_height), Image.ANTIALIAS)
st.title('Data Privacy API')
st.sidebar.image(image)

st.sidebar.info('"Data Privacy API" takes the text (and label, as optional item) as input, and returns matching value, data type, and corresponding regulation/compliance indications. With an “Data Privacy API”, we can feed it with any data we have, evaluate the risk and get consistent results quickly. ')


t = st.text_area('Enter message')
btn = st.button("Detect")

if btn:
    data_matchings = detect(t)
    if data_matchings:
        st.warning('Sensitive Item Detected')
        for m in data_matchings:
            m['offsets'] = allindices(t, m['value'])

        all_offsets = []
        offset2data = {}
        type2color = {}

        reqs = set()
        color_idx = 0
        for m in data_matchings:
            all_offsets += m['offsets']
            for r in m['requirements']:
                reqs.add(r)
            for o in m['offsets']:
                offset2data[o] = m
            if m['type'] not in type2color:
                type2color[m['type']] = colors[color_idx]
                color_idx += 1
                if color_idx >= len(colors):
                    color_idx = 0

        reqs = list(reqs)
        starting_index = 0
        seg = []
        all_offsets.sort()
        for idx, off in enumerate(all_offsets):
            if idx == 0:
                seg.append(t[0:off[0]])
            if idx > 0:
                seg.append(t[all_offsets[idx-1][1]: off[0]])
            data = offset2data[off]
            seg.append((data['value'], data['type'] + " "+ include_all(data['requirements']), type2color[data['type']]))


        if off[1] != len(t):
            seg.append(t[off[1]:])
        #print(annotated_text(*seg))
        annotated_text(*seg)
        st.markdown("**Policies**" + " : " + ", ".join(reqs))
    else:
        st.success("Pass.")
