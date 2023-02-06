""" This module provides you with useful date utility functions in the Chinese financial market for more convenient research purpose.

"""

import datetime
from datetime import date, timedelta


def get_market_time(now):
    """ Adjusted current datetime function.

    :param now: current datetime, e.g. datetime.datetime.now()
    :type now: datetime.datetime
    :return: corresponding market time, adjusting the dates that are not in the transaction
    :rtype: datetime.datetime
    """
    market_morning_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_morning_close = now.replace(hour=11, minute=30, second=0, microsecond=0)
    market_afternoon_open = now.replace(hour=13, minute=0, second=0, microsecond=0)
    market_afternoon_close = now.replace(hour=15, minute=0, second=0, microsecond=0)

    if now < market_morning_open:
        raise Exception("market not open yet")
    elif market_morning_open <= now <= market_morning_close:
        return now
    elif market_morning_close < now < market_afternoon_open:
        return market_morning_close
    elif market_afternoon_open <= now <= market_afternoon_close:
        return now
    else:
        return market_afternoon_close


def get_weekday_in_month(year, month, number_of_week, weekday):
    """ get the nth weekday in month

    :param year: year number, 'yyyy'
    :type year：int
    :param month: month number, 1-12
    :type month: int
    :param number_of_week: number of the week
    :type number_of_week: int
    :param weekday: weekday, 1-7. 1 represents monday, 7 represents sunday
    :type number_of_week: int
    :return: nth weekday in month
    :rtype: datetime.date
    """
    temp = date(year, month, 1)
    adj = (weekday - 1  - temp.weekday()) % 7
    temp += timedelta(days=adj)
    temp += timedelta(weeks=number_of_week-1)
    return temp


def date_from_string(date_str):
    """ Get datetime.date object from 'yyyymmdd' date string

    :param date_str: date string, e.g. "20220101"
    :type date_str: str, 'yyyymmdd'
    :return: date object
    :rtype: datetime.date
    """
    return date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))


def count_natural_days(start_date_str, end_date_str, include_start_date=False, include_end_date=True):
    """ Count the number of the natural days given string-like start date and date, with the inclusion of start date and end date represented by the specified boolean respectively

    :param start_date_str: start date string
    :type start_date_str: str, 'yyyymmdd'
    :param end_date_str: end date string
    :type end_date_str: str, 'yyyymmdd'
    :param include_start_date: determine whether to include the start date
    :type include_end_date: bool
    :param include_end_date: determine whether to include the end date
    :type include_end_date: bool
    :return: the number of natural days between start date and end date
    :rtype: int
    """

    start_date = date_from_string(start_date_str)
    end_date = date_from_string(end_date_str)
    days_to_add = 0
    if include_start_date:
        days_to_add += 1
    if include_end_date:
        days_to_add += 1

    return end_date - start_date - 1 + days_to_add

def count_business_days(start_date_str, end_date_str, cal, include_start_date=False, include_end_date=True):
    """ Count the number of business days given string-like start date and date, with the inclusion of start date and end date represented by the specified boolean respectively

    :param start_date_str: start date string
    :type start_date_str: str, 'yyyymmdd'
    :param end_date_str: end date string
    :type end_date_str: str, 'yyyymmdd'
    :param cal: calendar
    :type cal: optshare.Calendar
    :param include_start_date: determine whether to include the start date
    :type include_end_date: bool
    :param include_end_date: determine whether to include the end date
    :type include_end_date: bool
    :return: the number of natural days between start date and end date
    :rtype: int
    """

    start_date = date_from_string(start_date_str)
    end_date = date_from_string(end_date_str)
    return cal.business_days_between(start_date, end_date, include_start_date, include_end_date)


def add_months(input_date, months):
    month = input_date.month - 1 + months
    year = input_date.year + month // 12
    month = month % 12 + 1
    import calendar
    day = min(input_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def get_lastnth_trading_day(n, yyyy, mm, cal):
    """ Return the last nth trading day in month

    :param n: nth trading day
    :type n: int
    :param yyyy: 4-digit year number
    :type yyyy: int
    :param mm: month number, 1-12
    :type mm: int
    :param cal: calendar object
    :type cal: optshare.Calendar
    :return: the last nth trading day in month
    :rtype: datetime.date
    """
    next_month_first_date = add_months(date(yyyy, mm, 1), 1)
    d = next_month_first_date - timedelta(days=1)
    i = 0
    if cal.is_business_day(d):
        i += 1
    while i < n:
        d = cal.previous_business_day(d)
        i += 1
    return d


def get_nth_trading_day(n, yyyy, mm, cal):
    """ Return the nth trading day in month

    :param n: nth trading day
    :type n: int
    :param yyyy: 4-digit year number
    :type yyyy: int
    :param mm: month number, 1-12
    :type mm: int
    :param cal: calendar object
    :type cal: optshare.Calendar
    :return: the nth trading day in month
    :rtype: datetime.date
    """
    d = date(yyyy, mm, 1)
    i = 0
    if cal.is_business_day(d):
        i += 1
    while i < n:
        d = cal.next_business_day(d)
        i += 1
    return d


if __name__ == "__main__":
    from calendar_def import Calendar
    chinese_cal = Calendar()
    trading_days_between = count_business_days("20231001", "20231101", chinese_cal)
    print(trading_days_between)