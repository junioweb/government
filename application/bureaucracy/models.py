from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute
from pynamodb.models import Model


class Form(Model):
    form_id = UnicodeAttribute(hash_key=True, null=False)
    form_created_at = UTCDateTimeAttribute(range_key=True, null=False, default=datetime.now())
    form_attrs = JSONAttribute(null=False)

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
