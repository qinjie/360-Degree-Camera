import os

from chalice import *

from chalicelib.database.models import *

DEFAULT_COGNITO_IDENTITY_ID = os.environ.get('DEFAULT_COGNITO_IDENTITY_ID')

def get_cognito_id(identity):
    cognitoIdentityId = identity.get('cognitoIdentityId', DEFAULT_COGNITO_IDENTITY_ID)
    if not cognitoIdentityId:
        cognitoIdentityId = DEFAULT_COGNITO_IDENTITY_ID
    return cognitoIdentityId


def authorize_user(identity):
    cognito_id = get_cognito_id(identity)
    try:
        user_profile = AuthProvider.get(AuthProvider.cognito_id == cognito_id).user
        if user_profile.status == UserProfile.STATUS_PENDING:
            raise UnauthorizedError('You are pending for activation.')
        elif user_profile.status == UserProfile.STATUS_SUSPENDED:
            raise UnauthorizedError('You are suspended.')
        elif user_profile.status != UserProfile.STATUS_ACTIVE:
            raise UnauthorizedError('You are invalid user.')
        return user_profile
    except AuthProvider.DoesNotExist:
        raise UnauthorizedError('Sign-in user is not found.')


def authorize_teacher(user_profile):
    if not (user_profile.is_teacher()
        and user_profile.teacher_info[0].is_teacher()):
        raise ForbiddenError()


def authorize_admin(user_profile):
    if not (user_profile.is_admin()):
        raise ForbiddenError()


def authorize_manager(user_profile):
    if not (user_profile.is_teacher()
        and user_profile.teacher_info[0].is_manager()):
        raise ForbiddenError()


def authorize_caregiver(user_profile):
    if not user_profile.is_caregiver():
        raise ForbiddenError()


def authorize_caregiver_of_student(user_profile, student_id):
    try:
        (Caregiver.select()
                .where(Caregiver.user == user_profile)
                .where((Caregiver.account_type == Caregiver.TYPE_CAREGIVER)
                       | (Caregiver.account_type == Caregiver.TYPE_GUARDIAN))
                .where(Caregiver.student == student_id).get())
    except Caregiver.DoesNotExist:
        raise ForbiddenError()


def authorize_guardian_of_student(user_profile, student_id):
    try:
        (Caregiver.select()
                .where(Caregiver.user == user_profile)
                .where(Caregiver.account_type == Caregiver.TYPE_GUARDIAN)
                .where(Caregiver.student == student_id).get())
    except Caregiver.DoesNotExist:
        raise ForbiddenError()


def authorize_teacher_of_student(user_profile, student_id):
    try:
        (Student.select()
                .where(Student.id == student_id)
                .where(Student.centre == user_profile.teacher_info[0].centre).get())
    except Student.DoesNotExist:
        raise ForbiddenError()

