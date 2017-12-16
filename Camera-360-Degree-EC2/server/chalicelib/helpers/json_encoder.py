import json
from datetime import datetime, date, time
from dateutil import tz


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Singapore')

        if isinstance(obj, datetime):
            # return obj.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%I:%M %p')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
