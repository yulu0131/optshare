import os, requests
from datetime import datetime, timedelta
import warnings

class Calendar:
    def __init__(self, filename):
        self.filename = filename
        self.data_path = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(self.data_path, 'r') as f:
                holiday_dates = f.readlines()

        except FileNotFoundError:
            warnings.warn("Cannot recognize filename, use remote holiday list instead")
            response = requests.get(
         'https://raw.githubusercontent.com/yulu0131/optshare/master/src/optshare/date/China.txt')
            holiday_dates = list(filter(None, response.text.split('\n')))

        self._holiday_rule = [datetime.strptime(holiday_date.rstrip('\n'), "%Y-%m-%d").date() for holiday_date in holiday_dates]

    def is_business_day(self, input_date):
        return input_date.weekday()<5 and input_date not in self._holiday_rule

    def is_holiday(self, input_date):
        return not self.is_business_day(input_date)

    def next_business_day(self, input_date):
        while True:
            input_date = input_date + timedelta(days=1)
            if self.is_business_day(input_date):
                break
        return input_date

    def previous_business_day(self, input_date):
        while True:
            input_date = input_date - timedelta(days=1)
            if self.is_business_day(input_date):
                break
        return input_date

    def business_days_between(self, start_date, end_date):
        #todo: test remains
        if start_date > end_date:
            raise Exception("Start date is greater than end date!")
        current_date = start_date
        while current_date <= end_date:
            if self.is_business_day(current_date):
                yield current_date
            current_date = current_date + timedelta(days = 1)
        return current_date


if __name__ == '__main__':
    # test datafile
    cal = Calendar("China.txt")
    from datetime import date
    test_date = date(2023,10,1)
    justify_business_day = cal.is_business_day(test_date)
    justify_holiday = cal.is_holiday(test_date)
    next_businessday = cal.next_business_day(test_date)
    print(next_businessday)
