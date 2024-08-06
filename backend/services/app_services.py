from typing import Any
from fastapi import HTTPException


# Common class for application response and exception handling.
class ApplicationServices:
    @staticmethod
    def application_response(status_code: int, response_message: str = None,
                             success: bool = True, data: Any = None) -> dict:
        response = {
            "status_code": status_code,
            "response_message": response_message,
            "success": success,
            "data": data
        }
        return response

    @staticmethod
    def handle_exception(exception: Exception, is_raise: bool = True):
        response = {
            "status_code": 500,
            "response_message": str(exception),
            "success": False,
            "data": None
        }

        if isinstance(exception, HTTPException):
            response['status_code'] = exception.status_code
            response['response_message'] = exception.detail
        elif isinstance(exception, ValueError):
            response['status_code'] = 400
            response['response_message'] = str(exception)
        # Add more exception types if needed

        if is_raise:
            raise HTTPException(status_code=response['status_code'], detail=response['response_message'])
        else:
            return response
