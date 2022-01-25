#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
import pandas as pd

from model import Models
from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, request, jsonify
from supporting import (
    get_history_user,
    get_name_book,
    get_similar_name_book
)

INDEX_MODEL: int = 1

MODELS = [
    {
        'type': 0,
        'name': 'lightfm.sav'
    },
    {
        'type': 1,
        'name': 'implicit_1.sav'
    }
]
MODEL_TYPE: int = MODELS[INDEX_MODEL]['type']
MODEL_NAME: str = MODELS[INDEX_MODEL]['name']
MODEL_PATH: str = 'models/'
DATASET_PATH: str = 'data/medlib.json'
NAME_BOOKS: str = 'data/name_book_medlib.json'

df = pd.read_json(DATASET_PATH)
all_books = pd.read_json(NAME_BOOKS)

model_file = pickle.load(open(MODEL_PATH + MODEL_NAME, 'rb'))

model = Models(model_file=model_file, df=df, model_type=MODEL_TYPE)

# create app
app = Flask(__name__)

api = Api(app)

CORS(app)


@app.route('/api/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        json_data = json.loads(request.data, strict=False)

        if json_data is None:
            logging.info('Couldnt get response')

        user_id = json_data['user_id']

        if user_id is None:
            logging.info('Invalid data format')

        post_data = {}  # json for post query
        rec_name = []  # array for recommendation books
        hist_name = []  # array for recommendation books

        rec_ids = model.predict(user_id)
        hist_ids = get_history_user(user_id=user_id, df=df, all_books=all_books)

        for rec in rec_ids:
            rec_name.append(get_name_book(rec, all_books))

        for hist in hist_ids:
            hist_name.append(get_name_book(hist, all_books))

        post_data['rec_id'] = rec_ids
        post_data['rec_name'] = rec_name
        post_data['histoty_id'] = hist_ids
        post_data['history_name'] = hist_name

        if post_data is None:
            logging.info('Failed to create recommendation')

        return jsonify(post_data)


@app.route('/api/similar', methods=['POST'])
def similar():
    if request.method == 'POST':
        json_data = json.loads(request.data, strict=False)

        if json_data is None:
            logging.info('Couldnt get response')

        # try get user_id from json
        book_id = json_data['book_id']

        if book_id is None:
            logging.info('Invalid data format')

        post_data = {}
        similar_name = []
        similar_id = model.similar(book_id)

        for sim in similar_id:
            similar_name.append(get_similar_name_book(sim, df=df, all_books=all_books))

        post_data['sim_id'] = similar_id
        post_data['sim_name'] = similar_name

        return jsonify(post_data)


class Status(Resource):
    @staticmethod
    def get():
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


api.add_resource(Status, '/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
