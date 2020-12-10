#! /usr/bin/env python3.8
'''
Module sets formatting style of logs and sets the log level from an environment variable.

This file should be imported/called before any other modules that use any logging.
If any other modules that use logging are imported before this file,
then any calls to the logging module will not be formatted properly.
'''
import logging


def initialize_logger(log_level: str):
    '''Set logging level to the level specified in environment, and set formatting.

    Default to "INFO" if an invalid log_level value specified.'''
    # Note, do NOT do any logging in this function until the "basicConfig" is set!
    unable_to_set_user_log_level = False

    unset_aws_handlers()

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


def unset_aws_handlers():
    '''Unset handlers, so our custom log level will work.

    The following is a hack to get around the fact that AWS is setting
    log handlers without asking us, which prevents us from changing the level.'''
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
