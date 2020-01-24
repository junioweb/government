import os

from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute
from pynamodb.models import Model


class FormModel(Model):
    class Meta:
        table_name = os.environ['FORMS_TABLE']

    id = UnicodeAttribute(hash_key=True, null=False)
    created_at = UTCDateTimeAttribute(null=False, default=datetime.now())
    updated_at = UTCDateTimeAttribute(null=False)
    attrs = JSONAttribute(null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updated_at = datetime.now()
        super(FormModel, self).save()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
