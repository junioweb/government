import boto3
import logging
import os
import uuid

from datetime import datetime
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

FORMS_TABLE = os.environ['FORMS_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/forms/<string:form_id>")
def get_form(form_id):
    resp = client.get_item(
        TableName=FORMS_TABLE,
        Key={
            'form_id': {'S': form_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Form does not exist'}), 200

    return jsonify({
        'form_id': item.get('form_id').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/forms", methods=["POST"])
def create_form():
    form_id = str(uuid.uuid1())
    created_at = datetime.now().isoformat()
    attrs = request.json.get('attrs')
    if not attrs:
        logging.error('Validation Failed')
        return jsonify({'error_message': 'Couldn\'t create the form item. There is no \'attrs\' attribute.'}), 422

    client.put_item(
        TableName=FORMS_TABLE,
        Item={
            'form_id': {'S': form_id},
            'created_at': {'S': created_at},
            'attrs': {'S': attrs},
        }
    )

    return jsonify({
        'form_id': form_id,
        'created_at': created_at,
        'attrs': attrs,
    }), 201


@app.route("/forms")
def list_forms():
    resp = client.scan(TableName=FORMS_TABLE)

    return jsonify({
        'count': resp.get('Count').get('S'),
        'items': resp.get('Items'),
    })


if __name__ == "__main__":
    app.run()
