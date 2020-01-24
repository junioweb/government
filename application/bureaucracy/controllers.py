import logging
import uuid

from flask import Blueprint, jsonify, request
from pynamodb.exceptions import DeleteError, DoesNotExist

from .models import FormModel

bureaucracy = Blueprint('bureaucracy', __name__)


@bureaucracy.route('/', methods=['GET'])
def list_forms():
    results = FormModel.scan()

    return jsonify({
        'items': [dict(result) for result in results]
    })


@bureaucracy.route('/', methods=['POST'])
def create_form():
    id = str(uuid.uuid1())
    attrs = request.json.get('attrs')
    if not attrs:
        logging.error('Validation Failed')
        return jsonify({'error_message': 'Couldn\'t create the form item. There is no \'attrs\' attribute.'}), 422

    form = FormModel(id=id, attrs=attrs)
    form.save()

    return jsonify(dict(form)), 201


@bureaucracy.route('/<string:form_id>', methods=['GET'])
def get_form(form_id):
    try:
        found_form = FormModel.get(hash_key=form_id)
    except DoesNotExist:
        logging.error('Form id: %s was not found.' % form_id)
        return jsonify({})

    return jsonify(dict(found_form))


@bureaucracy.route('/<string:form_id>', methods=['PUT'])
def update_form(form_id):
    attrs = request.json.get('attrs')
    if not attrs:
        logging.error('Validation Failed')
        return jsonify({'error_message': 'Couldn\'t update the form item. There is no \'attrs\' attribute.'}), 422

    try:
        found_form = FormModel.get(hash_key=form_id)
    except DoesNotExist:
        logging.error('Form id: %s was not found.' % form_id)
        return jsonify({})

    form_changed = False
    if attrs != found_form.attrs:
        found_form.attrs = attrs
        form_changed = True

    if form_changed:
        found_form.save()
    else:
        logging.warning('Nothing changed did not update')

    return jsonify(dict(found_form))


@bureaucracy.route('/<string:form_id>', methods=['DELETE'])
def delete_form(form_id):
    try:
        found_form = FormModel.get(hash_key=form_id)
    except DoesNotExist:
        logging.error('Form id: %s was not found.' % form_id)
        return jsonify({})

    try:
        found_form.delete()
    except DeleteError:
        return jsonify({'error_message': 'Unable to delete the Form'}), 400

    return '', 204
