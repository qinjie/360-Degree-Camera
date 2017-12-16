from chalice import Response
import json

FORBIDDEN = 403
UNAUTHORIZED = 401
NOT_FOUND = 404
BAD_REQUEST = 400
INTERNAL_ERROR = 500

CONTENT_JSON = {
    'Content-Type': 'application/json'
}


def forbidden(message='You are not allowed to perform this action.'):
    if message.startswith('ForbiddenError: '):
        message = message.replace('ForbiddenError: ', '')
    return Response(
        body=json.dumps({
            'message': message
        }),
        status_code=FORBIDDEN,
        headers=CONTENT_JSON
    )


def unauthorized(message='You are not authorized.'):
    if message.startswith('UnauthorizedError: '):
        message = message.replace('UnauthorizedError: ', '')
    return Response(
        body=json.dumps({
            'message': message
        }),
        status_code=UNAUTHORIZED,
        headers=CONTENT_JSON
    )


def not_found(message='Data is not found.'):
    return Response(
        body=json.dumps({
            'message': message
        }),
        status_code=NOT_FOUND,
        headers=CONTENT_JSON
    )


def bad_request(message='Invalid data.'):
    if message.startswith('BadRequestError: '):
        message = message.replace('BadRequestError: ', '')
    return Response(
        body=json.dumps({
            'message': message
        }),
        status_code=BAD_REQUEST,
        headers=CONTENT_JSON
    )


def internal_error(message='The server encountered an internal error.'):
    return Response(
        body=json.dumps({
            'message': message
        }),
        status_code=INTERNAL_ERROR,
        headers=CONTENT_JSON
    )
