from django.db import models
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)
import os


class ExchangeRates(Model):
    class Meta:
        table_name = 'Exchange_Rates'
        host = os.environ.get('DYNAMO_DB_HOST')

        # might change this later
        write_capacity_units = 1
        read_capacity_units = 1

    currency = UnicodeAttribute(hash_key=True)
    rate = NumberAttribute()
    date = UTCDateTimeAttribute()
    dayNumber = NumberAttribute(range_key=True)
