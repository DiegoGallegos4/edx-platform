"""
Provides Python APIs exposed from Bulk Email models.
"""
from bulk_email.models import BulkEmailFlag, CourseAuthorization, Optout


def is_user_opted_out_for_course(user, course_id):
    """
    Arguments:
        user: user whose opt out status is to be returned
        course_id (CourseKey): id of the course

    Returns:
        bool: True if user has opted out of e-mails for the course
        associated with course_id, False otherwise.
    """
    return Optout.objects.filter(
        user=user,
        course_id=course_id,
    ).exists()


def is_bulk_email_feature_enabled(course_id=None):
    """
    Looks at the currently active configuration model to determine whether the bulk email feature is available.

    Arguments:
        course_id (string; optional): the course id of the course

    Returns:
        bool: True or False, depending on the following:
            If the flag is not enabled, the feature is not available.
            If the flag is enabled, course-specific authorization is required, and the course_id is either not provided
                or not authorixed, the feature is not available.
            If the flag is enabled, course-specific authorization is required, and the provided course_id is authorized,
                the feature is available.
            If the flag is enabled and course-specific authorization is not required, the feature is available.
    """
    if not BulkEmailFlag.is_enabled():
        return False
    elif BulkEmailFlag.current().require_course_email_auth:
        if course_id is None:
            return False
        else:
            return is_bulk_email_enabled_for_course(course_id)
    else:  # implies enabled == True and require_course_email == False, so email is globally enabled
        return True


def is_bulk_email_enabled_for_course(course_id):
    """
    Arguments:
        course_id: the course id of the course

    Returns:
        bool: True if the Bulk Email feature is enabled for the course
        associated with the course_id; False otherwise
    """
    try:
        record = CourseAuthorization.objects.get(course_id=course_id)
        return record.email_enabled
    except CourseAuthorization.DoesNotExist:
        return False
