import os, requests
from datetime import datetime, timedelta
import warnings


class Calendar:
    """ This module provides the interface for determining whether a date is business day or holiday via specifying a txt file with holiday list.

    """

    def __init__(self, filename=None):
        """ Specify holiday list with a txt file

        :param filename: a txt file with holiday list, use remote url instead if cannot find file or filename is None
        :type filename: str or None
        """
        self.filename = filename

        try:
            if self.filename is None:
                response = requests.get(
                    'https://raw.githubusercontent.com/yulu0131/optshare/master/src/optshare/dateutils/China.txt')
                holiday_dates = list(filter(None, response.text.split('\n')))

            else:
                data_path = os.path.join(os.path.dirname(__file__), self.filename)
                with open(data_path, 'r') as f:
                    holiday_dates = f.readlines()

        except FileNotFoundError:
            warnings.warn("Cannot recognize filename, use remote Chinese holiday list instead")
            response = requests.get(
                'https://raw.githubusercontent.com/yulu0131/optshare/master/src/optshare/dateutils/China.txt')
            holiday_dates = list(filter(None, response.text.split('\n')))

        self._holiday_rule = [datetime.strptime(holiday_date.rstrip('\n'), "%Y-%m-%d").date() for holiday_date in
                              holiday_dates]

    def is_business_day(self, d):
        """ A boolean value that determines whether d is business day

        :param d: input date
        :type d: datetime.date
        :return: True or False. True if d is business day, and vice versa.
        :rtype: bool
        """
        return d.weekday() < 5 and d not in self._holiday_rule

    def is_holiday(self, d):
        """ A boolean value that determines whether d is holiday

        :param d: input date
        :type d: datetime.date
        :return: True or False. True if d is holiday, and vice versa.
        :rtype: bool
        """
        return not self.is_business_day(d)

    def next_business_day(self, d):
        """ Returns the following business day given input date d

        :param d: input date
        :type d: datetime.date
        :return: next business day
        :rtype: datetime.date
        """
        while True:
            d = d + timedelta(days=1)
            if self.is_business_day(d):
                break
        return d

    def previous_business_day(self, d):
        """ Returns previous business day given input date d

        :param d: input date
        :type d: datetime.date
        :return: previous business day
        :type: datetime.date
        """
        while True:
            d = d - timedelta(days=1)
            if self.is_business_day(d):
                break
        return d

    def business_days_between(self, start_date, end_date, include_start_date=False, include_end_date=True):
        """ Count the number of business days between given start date and end date, specifying whether to include start date or end date

        :param start_date: start date
        :type start_date: datetime.date
        :param end_date: end date
        :type end_date: datetime.date
        :param include_start_date: determine whether to include start date
        :type include_start_date: bool
        :param include_end_date: determine whether to include end date
        :type include_end_date: bool
        :return: the number of business days between start date and end date
        :rtype: bool
        """

        if start_date > end_date:
            raise Exception("Start date is greater than end date!")

        current_date = start_date
        days = 0
        while current_date <= end_date:
            if self.is_business_day(current_date):
                days += 1
            current_date = current_date + timedelta(days=1)

        if not include_start_date:
            days -= 1
        if not include_end_date:
            days -= 1
        return days


if __name__ == '__main__':
    # test datafile
    cal = Calendar()
    from datetime import date

    date1 = date(2023, 10, 1)
    date2 = date(2023, 11, 1)
    # justify_business_day = cal.is_business_day(test_date)
    # justify_holiday = cal.is_holiday(test_date)
    days_between = cal.business_days_between(date1, date2)
    print("optshare results is ", days_between)
