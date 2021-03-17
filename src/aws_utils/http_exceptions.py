#!/usr/bin/env python3.8
'''
This module contains useful Exceptions for lambda functions
'''
from http import HTTPStatus
from typing import Optional


class ServerError(Exception):
    '''Parent class for HTTP Error Responses.

    Any child classes should define self.error_status.'''
    error_status: Optional[HTTPStatus] = None

    def __init__(self, message=None, errors=None):
        super().__init__(message)

        if self.error_status is None:
            err_name = self.__class__.__name__
            raise NotImplementedError(
                f'You must assign an HTTPStatus to self.error_status for Error "{err_name}"'
            )

        self.message = message
        self.errors = errors

    def __str__(self):
        '''Prepend error code to error message.

        AWS looks for regex patterns in the string representation of the error message
        to determine the appropriate error code. We prepend the error code to the string
        so that AWS can match the string and return the corresponding code to the user.'''
        if self.message:
            return f'{self.error_status.value}: {self.message}'
        else:
            return f'{self.error_status.value}'


class BadRequest(ServerError):
    '''Generic exception for requests that are malformed.'''
    error_status = HTTPStatus.BAD_REQUEST


class InternalServerError(ServerError):
    '''Generic exception for internal errors while processing requests.'''
    error_status = HTTPStatus.INTERNAL_SERVER_ERROR
