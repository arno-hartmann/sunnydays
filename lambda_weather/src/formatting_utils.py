from decimal import *
from datetime import date, timedelta, datetime


def maketimestring(day):
    date = day.strftime("%Y/%m/%d")
    return date

def strtime_to_timestamp(data):
    timestamp = datetime.timestamp(data)
    return timestamp

def is_date_recent(data):
    day = date.today()
    yesterday = day - timedelta(days = 2)
    t = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
    return t.date() > yesterday

def make_decimal(data):
    if data:
        decimal = round(Decimal(data),2)
        return decimal