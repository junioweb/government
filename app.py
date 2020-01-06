import os
import boto3

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
            'formId': {'S': form_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Form does not exist'}), 200

    return jsonify({
        'formId': item.get('formId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/forms", methods=["POST"])
def create_form():
    form_id = request.json.get('formId')
    name = request.json.get('name')
    if not form_id or not name:
        return jsonify({'error': 'Please provide formId and name'}), 400

    client.put_item(
        TableName=FORMS_TABLE,
        Item={
            'formId': {'S': form_id},
            'name': {'S': name}
        }
    )

    return jsonify({
        'formId': form_id,
        'name': name
    })


if __name__ == "__main__":
    app.run()
