import datetime
def get_market_time(now):
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


def date_from_string(date_str):
    """
    :param date_str: dateutils string, e.g. "2022-01-01"
    :return: datetime.dateutils
    """
    return datetime.date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:10]))


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
    temp = datetime.date(year, month, 1)
    adj = (weekday - temp.weekday()) % 7 - 1
    temp += datetime.timedelta(days=adj)
    temp += datetime.timedelta(weeks=number_of_week - 1)
    return temp



# def count_days(start_date_str, end_date_str, calendar_type, include_start_date=False, include_end_date=True):
#     start_date = date_from_string(start_date_str)
#     end_date = date_from_string(end_date_str)
#     days_to_add = 0
#     if include_start_date:
#         days_to_add += 1
#     if include_end_date:
#         days_to_add += 1
#     if calendar_type == '自然日':
#         return end_date - start_date - 1 + days_to_add
#     if calendar_type == '交易日':
#         return calendar.business_days_between(start_date, end_date, include_start_date, include_end_date)
#
#
# def get_lastnth_trading_day(n, yyyy, mm, cal):
#     next_month_first_date = opt.Date(yyyy, mm, 1) + opt.Months(1)
#     d = next_month_first_date - opt.Days(1)
#     i = 0
#     if cal.is_businessday(d):
#         i += 1
#     while i < n:
#         d = cal.previous_businessday(d)
#         i += 1
#     return d
#
#
# def get_nth_trading_day(n, yyyy, mm, cal):
#     d = opt.Date(yyyy, mm, 1)
#     i = 0
#     if cal.is_businessday(d):
#         i += 1
#     while i < n:
#         d = cal.next_businessday(d)
#         i += 1
#     return d

if __name__ == "__main__":

    print(get_weekday_in_month(2023, 2, 4, 1))
