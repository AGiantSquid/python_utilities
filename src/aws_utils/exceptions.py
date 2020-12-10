#!/usr/bin/env python3.8
'''
This module contains useful Exceptions for lambda functions
'''


class ServerError(Exception):
    '''Parent class for HTTP Error Responses.

    Any child classes should define self.error_code.'''
    error_code = None

    def __init__(self, message=None, errors=None):
        super().__init__(message)

        if self.error_code is None:
            raise NotImplementedError(
                f'You must assign a number to self.error_code for Error "{self.__class__.__name__}"'
            )

        self.message = message
        self.errors = errors

    def __str__(self):
        '''Prepend error code to error message.

        AWS looks for regex patterns in the string representation of the error message
        to determine the appropriate error code. We prepend the error code to the string
        so that AWS can match the string and return the corresponding code to the user.'''
        if self.message:
            return f'{self.error_code}: {self.message}'
        else:
            return f'{self.error_code}'


class BadRequest(ServerError):
    '''Generic exception for requests that are malformed.'''
    error_code = 400


class InternalServerError(ServerError):
    '''Generic exception for internal errors while processing requests.'''
    error_code = 500
