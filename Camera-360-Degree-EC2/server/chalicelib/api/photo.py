from chalice import *
from datetime import date

from chalicelib.services import photo, caregiver_invitation, caregiver
from chalicelib.helpers import auth
from chalicelib.database.models import *


def get_photos(query, body, node_id):
    query = query if query else {}

    page_num = int(query.get('page', 1))
    items_per_page = int(query.get('limit', 10))
    return photo.list_by_node(node_id, page_num, items_per_page)


def add_photo(query, body):
    user_centre = auth_user.teacher_info[0].centre
    return photo.add_in_centre(user_centre, body)


def get_one_student(student_id, query, body, auth_user):
    try:
        auth.authorize_teacher(auth_user)
        user_centre = auth_user.teacher_info[0].centre
        return photo.get_in_centre_by_id(user_centre, student_id)
    except Student.DoesNotExist:
        raise NotFoundError()


def update_student(student_id, query, body, auth_user):
    auth.authorize_teacher(auth_user)
    user_centre = auth_user.teacher_info[0].centre;
    result = photo.update_in_centre_by_id(user_centre, student_id, body)
    if result != 1:
        raise NotFoundError()
    return photo.get_in_centre_by_id(user_centre, student_id)


def delete_student(student_id, query, body, auth_user):
    try:
        auth.authorize_manager(auth_user)
        user_centre = auth_user.teacher_info[0].centre
        return photo.delete_in_centre(user_centre, student_id)
    except Student.DoesNotExist:
        raise NotFoundError()


def get_by_serial(serial, query, body, auth_user):
    try:
        query = query if query else {}
        auth.authorize_teacher(auth_user)
        user_centre = auth_user.teacher_info[0].centre
        health_check_day = query.get('date')
        return photo.get_in_centre_by_serial(user_centre, serial, health_check_day)
    except Student.DoesNotExist:
        raise NotFoundError()


def get_upload_url(student_id, query, body, auth_user):
    if auth_user.is_caregiver():
        auth.authorize_caregiver_of_student(auth_user, student_id)
    elif auth_user.is_teacher():
        auth.authorize_teacher_of_student(auth_user, student_id)

    return photo.get_upload_url(student_id)



