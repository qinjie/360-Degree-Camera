import uuid
from chalice import *
from playhouse.shortcuts import model_to_dict

from chalicelib.database.models import *
from chalicelib.helpers.main_helpers import *
from chalicelib.services import class_group, caregiver, aws


def list_by_node(node, page_num, items_per_page):
    students = (Student.select(Student, ClassGroup, ClassLevel)
                .join(ClassGroup).join(ClassLevel)
                .where(Student.centre == centre)
                .where(Student.fullname.contains(fullname))
                .where(Student.status == Student.STATUS_ACTIVE)
                .order_by(Student.fullname)
                .paginate(page_num, items_per_page))
    if group_id:
        students = students.where(Student.current_group == group_id)

    result = {}
    for student in students:
        result[student.id] = model_to_dict(student,
                                           only=[Student.id] + Student.detail_fields
                                                + [Student.current_group, ClassGroup.id] + ClassGroup.detail_fields
                                                + [ClassGroup.current_level] + ClassLevel.detail_fields)
        result[student.id]['profile_image'] = None
        result[student.id]['caregivers'] = caregiver.list_by_student(student.id)
        if health_check_day:
            result[student.id]['visual_check'] = None
            result[student.id]['today_attendance'] = None

    student_ids = result.keys()
    files = (File.select(File.centre, File.model_id, File.model_name, File.title,
                         File.created_at)
             .where(File.model_name == File.MODEL_STUDENT)
             .where(File.model_id << student_ids)
             .where(File.type == File.TYPE_STUDENT_LATEST_PHOTO).dicts())

    for file in files:
        result[file['model_id']]['profile_image'] = {
            'origin_url': get_image_origin_url(file),
            'thumbnail_url': get_image_thumbnail_url(file),
            'created_at': file['created_at']
        }

    if health_check_day:
        visual_checks = (VisualCheck.select(VisualCheck.student, VisualCheck.status)
                         .where(VisualCheck.student << student_ids)
                         .where(VisualCheck.on_date == health_check_day).dicts())
        for visual_check in visual_checks:
            result[visual_check['student']]['visual_check'] = {
                'status': visual_check['status']
            }

        attendances = (Attendance.select(Attendance, LeaveApplication,
                                         Student, UserProfile)
                       .join(LeaveApplication, JOIN.LEFT_OUTER)
                       .join(Student, on=(Attendance.student == Student.id))
                       .join(UserProfile, JOIN.LEFT_OUTER,
                             on=(Attendance.check_in_by == UserProfile.id))
                       .where(Attendance.student << student_ids)
                       .where(Attendance.on_date == health_check_day))

        for attendance in attendances:
            item = model_to_dict(attendance,
                                 only=[Attendance.id, Attendance.check_in_time, Attendance.status]
                                      + [Attendance.check_in_by, UserProfile.id]
                                      + [Attendance.leave_application] + LeaveApplication.detail_fields)
            result[attendance.student.id]['today_attendance'] = item
    return result.values()


def to_dict(model, for_caregiver=False):
    extracted_fields = ([Student.id] + Student.detail_fields
                        + [Student.current_group, ClassGroup.id] + ClassGroup.detail_fields
                        + [ClassGroup.current_level] + ClassLevel.detail_fields)
    if for_caregiver:
        extracted_fields += [Student.centre] + Centre.detail_fields

    result = model_to_dict(model, only=extracted_fields)

    result['caregivers'] = caregiver.list_by_student(result['id'])

    try:
        file = (File.select()
                .where(File.model_name == Student._meta.db_table)
                .where(File.model_id == model.id)
                .where(File.type == File.TYPE_STUDENT_LATEST_PHOTO).get())
        result['profile_image'] = {
            'origin_url': file.get_origin_url(),
            'thumbnail_url': file.get_thumbnail_url(),
            'created_at': file.created_at
        }
    except File.DoesNotExist:
        result['profile_image'] = None

    return result


def get_in_centre_by_id(centre, id):
    model = (Student.select(Student, ClassGroup, ClassLevel, Centre)
             .join(ClassGroup).join(ClassLevel)
             .join(Centre, on=(Student.centre == Centre.id))
             .where(Student.id == id)
             .where(Student.status == Student.STATUS_ACTIVE).get())
    if model.centre != centre:
        raise ForbiddenError('You are not allowed to perform this action.')

    return to_dict(model)


def get_in_centre_by_serial(centre, serial, health_check_day):
    model = (Student.select(Student, ClassGroup, ClassLevel, Centre)
             .join(ClassGroup).join(ClassLevel)
             .join(Centre, on=(Student.centre == Centre.id))
             .where(Student.serial == serial)
             .where(Student.status == Student.STATUS_ACTIVE).get())
    if model.centre != centre:
        raise ForbiddenError('You are not allowed to perform this action.')

    result = to_dict(model)

    try:
        visual_check = (VisualCheck.select(VisualCheck.status)
                        .where(VisualCheck.student == model)
                        .where(VisualCheck.on_date == health_check_day).get())
        result['visual_check'] = {
            'status': visual_check['status']
        }
    except VisualCheck.DoesNotExist:
        result['visual_check'] = None

    try:
        attendance = (Attendance.select(Attendance, LeaveApplication,
                                        Student, UserProfile)
                      .join(LeaveApplication, JOIN.LEFT_OUTER)
                      .join(Student, on=(Attendance.student == Student.id))
                      .join(UserProfile, JOIN.LEFT_OUTER,
                            on=(Attendance.check_in_by == UserProfile.id))
                      .where(Attendance.student == model)
                      .where(Attendance.on_date == health_check_day).get())

        result['today_attendance'] = model_to_dict(attendance,
                                                   only=[Attendance.id, Attendance.check_in_time, Attendance.status]
                                                        + [Attendance.check_in_by, UserProfile.id]
                                                        + [
                                                            Attendance.leave_application] + LeaveApplication.detail_fields)
    except Attendance.DoesNotExist:
        result['today_attendance'] = None

    return result


def add_in_centre(centre, student):
    current_group = class_group.get_in_centre(centre, student['current_group'])
    student['centre'] = centre
    student['serial'] = uuid.uuid4()
    row = Student.create(**student)

    row.sns_topic = aws.create_topic('student-{0}'.format(row.id))
    row.save()
    return to_dict(row)


def update_in_centre_by_id(centre, id, student):
    student = ignore_keys(student, Student.ignored_updated_fields)
    return (Student.update(**student)
            .where(Student.id == id)
            .where(Student.centre == centre)
            .execute())


def delete_in_centre(centre, id):
    student = (Student.select()
               .where(Student.id == id).get())
    if student.centre != centre:
        raise ForbiddenError('You are not allowed to perform this action.')

    aws.delete_topic(student.sns_topic)

    student.status = Student.STATUS_INACTIVE
    student.save()


def get_kids_for_checkinout(user_id, check_day):
    kids = (Student.select(Student, ClassGroup, ClassLevel)
            .join(ClassGroup).join(ClassLevel)
            .join(Caregiver, on=(Caregiver.student == Student.id))
            .where(Caregiver.user == user_id)
            .where(Student.status == Student.STATUS_ACTIVE))

    result = {}
    for kid in kids:
        result[kid.id] = model_to_dict(kid,
                                       only=[Student.id, Student.fullname, Student.gender]
                                            + [Student.current_group] + ClassGroup.detail_fields
                                            + [ClassGroup.current_level] + ClassLevel.detail_fields)
        result[kid.id]['check_in_out'] = None
        result[kid.id]['profile_image'] = None

    kid_ids = result.keys()
    files = (File.select()
             .where(File.model_name == Student._meta.db_table)
             .where(File.model_id << kid_ids)
             .where(File.type == File.TYPE_STUDENT_LATEST_PHOTO).dicts())

    for file in files:
        result[file['model_id']]['profile_image'] = {
            'origin_url': get_image_origin_url(file),
            'thumbnail_url': get_image_thumbnail_url(file),
            'created_at': file['created_at']
        }

    attendances = (Attendance.select(Attendance, LeaveApplication)
                   .join(LeaveApplication, JOIN.LEFT_OUTER)
                   .where(Attendance.student << kid_ids)
                   .where(Attendance.on_date == check_day).aggregate_rows())

    for attendance in attendances:
        result[attendance.student.id]['check_in_out'] = (
            model_to_dict(attendance,
                          only=[Attendance.id, Attendance.status, Attendance.check_in_time, Attendance.check_out_time,
                                Attendance.remark]
                               + [Attendance.leave_application] + LeaveApplication.detail_fields)
        )

    temperatures = (Temperature.select()
                    .where(Temperature.student << kid_ids)
                    .where(Temperature.on_date == check_day)
                    .where(Temperature.check_by == user_id).dicts())
    for temperature in temperatures:
        result[temperature['student']]['check_in_out']['temperature'] = temperature['celsius']

    return result.values()

