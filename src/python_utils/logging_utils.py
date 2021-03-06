#! /usr/bin/env python3
'''
Module sets formatting style of logs and sets the log level from an environment variable.

This file should be imported/called before any other modules that use any logging.
If any other modules that use logging are imported before this file,
then any calls to the logging module will not be formatted properly.
'''
import logging
from functools import wraps


def initialize_logger(log_level: str, remove_existing_handlers=False):
    '''Set logging level to the level specified in environment, and set formatting.

    Default to "INFO" if an invalid log_level value specified.'''
    # Note, do NOT do any logging in this function until the "basicConfig" is set!
    unable_to_set_user_log_level = False

    if remove_existing_handlers:
        remove_handlers()

    upper_case_level = log_level.upper()

    try:
        logging_level = getattr(logging, upper_case_level)
    except AttributeError:
        unable_to_set_user_log_level = True
        logging_level = logging.INFO

    logging.basicConfig(
        level=logging_level,
        format='%(levelname)-8s - %(asctime)s - %(name)s - %(message)s',
    )

    logging.info('Logger initialized! Threshold set to "%s".',
                 logging.getLevelName(logging_level))

    if unable_to_set_user_log_level:
        logging.warning(
            'User attempted to set log level to "%s", which is not a valid log level!', log_level)


def remove_handlers():
    '''Unset handlers, so our custom log level will work.

    The following is a hack to get around the fact that AWS is setting
    log handlers without asking us, which prevents us from changing the level.'''
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

class LazyString(object):
    '''Postpone function evaluation until it is stringified.'''

    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def __str__(self):
        return '{0}'.format(self.func(*self.args))


def lazy_evaluate_string(func):
    '''Return class that only evaluates input function when stringified.

    Decorate function that returns string when using with logger.'''

    @wraps(func)
    def wrapper(*args):
        dm = LazyString(func, *args)
        return dm

    return wrapper
