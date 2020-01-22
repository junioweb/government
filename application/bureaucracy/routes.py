from flask import jsonify
from .dao import FormDAO

DAO = FormDAO()


@bp.route('/', methods='GET')
def list_forms():
    results = DAO.list()

    return jsonify({
        'items': [dict(result) for result in results]
    })
