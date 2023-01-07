from datetime import datetime, date


def get_day_number(ZERO_DATE="22-12-31"):
    parsed_zero_date = datetime.strptime(ZERO_DATE, "%y-%m-%d")
    today = datetime.now()

    delta = today - parsed_zero_date
    return delta.days


def is_true(property):
    return property in ['true', True, 'True']
