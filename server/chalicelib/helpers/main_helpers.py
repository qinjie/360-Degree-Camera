import random
import string
from datetime import datetime, date, time, timedelta


def ignore_keys(data, ignored_keys):
    if not data:
        return data
    result = {}
    for key, value in data.items():
        if not key in ignored_keys:
            result[key] = value
    return result


def equal_month_year(date1, date2):
    return date1.month == date2.month and date1.year == date2.year


def is_not_sunday(date):
    return date.weekday() != 6


def normalize_fields_in_dict(model, data):
    result = {}
    for key in data.keys():
        field = getattr(model, key)
        result[field.name] = data[key]
    return result


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def convert_datetime(d):
    if not d:
        return d
    if isinstance(d, list):
        return [convert_datetime(item) for item in d]
    result = {}
    for key, value in d.items():
        if isinstance(value, (list, dict)):
            result[key] = convert_datetime(value)
        elif isinstance(value, datetime):
            result[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            result[key] = value.strftime('%Y-%m-%d')
        elif isinstance(value, time):
            result[key] = value.strftime('%I:%M %p')
        else:
            result[key] = value
    return result


def datetime_relative_today_string(dt):
    if dt.date() == date.today():
        return dt.strftime('%I:%M %p')
    else:
        return dt.strftime('%b %d, %I:%M %p')


def generate_random_digits(number_digits):
    return ''.join(random.choice(string.digits) for _ in range(number_digits))


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)
