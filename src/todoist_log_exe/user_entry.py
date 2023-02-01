"""Collect params from user.

:author: Shay Hill
:created: 2023-02-01
"""

import datetime
from typing import NamedTuple

DEFAULT_BEG_DATE_DELTA = 8
DEFAULT_BEG_TIME = "00:00:00"
DEFAULT_END_DATE_DELTA = 1
DEFAULT_END_TIME = "23:59:59"


def _input_date(prompt: str, default_delta: int) -> datetime.date:
    """Prompt the user for a date. Repeat prompt until a valid date is entered.

    :param prompt: The prompt to display to the user.
    :param default_delta: The number of days to subtract from today's date to create
        a default value.
    :return: The date entered by the user.
    """
    prompt += f" (Enter for default: {default_delta} day(s) ago): "
    while True:
        datestr = input(prompt)
        if not datestr:
            return datetime.date.today() - datetime.timedelta(days=default_delta)
        try:
            return datetime.datetime.strptime(datestr, "%y%m%d").date()
        except ValueError:
            print("That didn't work. Ensure correct input format: YYMMDD.")


def _input_time(prompt: str, default_str: str) -> datetime.time:
    """Prompt the user for a time. Repeat prompt until a valid time is entered.

    :param prompt: The prompt to display to the user.
    :param default_str: The default time to use if the user enters nothing.
    :return: The time entered by the user.
    """
    prompt += f" (Enter for default: {default_str}): "
    while True:
        time_str = input(prompt)
        if not time_str:
            return datetime.datetime.strptime(default_str, "%H:%M:%S").time()
        try:
            return datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        except ValueError:
            print("That didn't work. Ensure correct input format: HH:MM:SS.")


def _input_beg_date() -> datetime.date:
    """Prompt the user for a start date.

    :return: The date entered by the user.
    """
    return _input_date("Start date (YYMMDD)?", DEFAULT_BEG_DATE_DELTA)


def _input_beg_time() -> datetime.time:
    """Prompt the user for a start time.

    :return: The time entered by the user.
    """
    return _input_time("Start time (HH:MM:SS)?", DEFAULT_BEG_TIME)


def _input_end_date() -> datetime.date:
    """Prompt the user for an end date.

    :return: The date entered by the user.
    """
    return _input_date("End date (YYMMDD)?", DEFAULT_END_DATE_DELTA)


def _input_end_time() -> datetime.time:
    """Prompt the user for an end time.

    :return: The time entered by the user.
    """
    return _input_time("End time (HH:MM:SS)?", DEFAULT_END_TIME)


def _date_time_to_timestamp(date: datetime.date, time: datetime.time) -> str:
    """Convert date and time to timestamp Todoist will understand.

    :param date: Date to convert.
    :param time: Time to convert.
    :return: Timestamp in format YYYY-MM-DDTHH:MM:SS
    """
    datetime_ = datetime.datetime.combine(date, time)
    return datetime_.strftime("%Y-%m-%dT%H:%M:%S")


class ApiArgs(NamedTuple):
    """Arguments to pass to Todoist API.

    :param api_token: API token to use.
    :param since: Timestamp in format YYYY-MM-DDTHH:MM:SS to use as start of time range.
    :param until: Timestamp in format YYYY-MM-DDTHH:MM:SS to use as end of time range.
    """

    api_token: str
    since: str
    until: str


def get_api_args() -> ApiArgs:
    """Prompt the user for arguments to pass to the Todoist API.

    :return: Arguments to pass to the Todoist API.
    """
    api_token = input("Enter your Todoist API token: ")
    beg_date = _input_beg_date()
    beg_time = _input_beg_time()
    end_date = _input_end_date()
    end_time = _input_end_time()
    since = _date_time_to_timestamp(beg_date, beg_time)
    until = _date_time_to_timestamp(end_date, end_time)
    return ApiArgs(api_token, since, until)
