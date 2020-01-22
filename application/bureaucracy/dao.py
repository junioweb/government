import boto3
import logging
import os

from .models import Form

FORMS_TABLE = os.environ['FORMS_TABLE']
client = boto3.client('dynamodb')


class FormDAO(object):
    def list(self):
        logging.info('List forms')
        return Form.scan()
