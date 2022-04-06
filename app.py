from flask import Flask, render_template, flash, request, jsonify
import spacy
import spacy_udpipe
import sys
import gunicorn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def getConll(texts):
    #nlp = spacy.load("en_core_web_sm")
    nlp = spacy_udpipe.load("en")
    from spacy import displacy

    from spacy_conll import init_parser

    con = init_parser(
        "en", "udpipe", include_headers=True
    )

    text = texts.rstrip()
    doc = nlp(text)
    doc_con = con(text)

    conll = doc_con._.conll_str

    return conll

@app.route('/hello')
def hello():
    text = getConll(request.args.get('phrase'))
    return jsonify({"result":text})