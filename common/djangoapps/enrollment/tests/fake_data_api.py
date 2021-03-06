"""
A Fake Data API for testing purposes.
"""
import copy
import datetime


_DEFAULT_FAKE_MODE = {
    "slug": "honor",
    "name": "Honor Code Certificate",
    "min_price": 0,
    "suggested_prices": "",
    "currency": "usd",
    "expiration_datetime": None,
    "description": None
}

_ENROLLMENTS = []

_COURSES = []

_ENROLLMENT_ATTRIBUTES = []

_VERIFIED_MODE_EXPIRED = []


# pylint: disable=unused-argument
def get_course_enrollments(student_id, org_filter=None):
    """Stubbed out Enrollment data request."""
    res = _ENROLLMENTS

    # apply ORG filter, if specified
    # NOTE, do not do a Falsy type check here because an empty list
    # and None do not have the same semantic meaning. None means no filtering.
    # Empty list means 'filter everything out'
    if org_filter is not None:
        _set = []
        for enrollment in _ENROLLMENTS:
            for org in org_filter:
                if org in enrollment['course']['course_id']:
                    _set.append(enrollment)
        res = _set

    return res


def get_course_enrollment(student_id, course_id):
    """Stubbed out Enrollment data request."""
    return _get_fake_enrollment(student_id, course_id)


def create_course_enrollment(student_id, course_id, mode='honor', is_active=True):
    """Stubbed out Enrollment creation request. """
    return add_enrollment(student_id, course_id, mode=mode, is_active=is_active)


def update_course_enrollment(student_id, course_id, mode=None, is_active=None):
    """Stubbed out Enrollment data request."""
    enrollment = _get_fake_enrollment(student_id, course_id)
    if enrollment and mode is not None:
        enrollment['mode'] = mode
    if enrollment and is_active is not None:
        enrollment['is_active'] = is_active
    return enrollment


def get_course_enrollment_info(course_id, include_expired=False):
    """Stubbed out Enrollment data request."""
    return _get_fake_course_info(course_id, include_expired)


def _get_fake_enrollment(student_id, course_id):
    """Get an enrollment from the enrollments array."""
    for enrollment in _ENROLLMENTS:
        if student_id == enrollment['student'] and course_id == enrollment['course']['course_id']:
            return enrollment


def _get_fake_course_info(course_id, include_expired=False):
    """Get a course from the courses array."""
    # if verified mode is expired and include expired is false
    # then remove the verified mode from the course.
    for course in _COURSES:
        if course_id == course['course_id']:
            if course_id in _VERIFIED_MODE_EXPIRED and not include_expired:
                course['course_modes'] = [mode for mode in course['course_modes'] if mode['slug'] != 'verified']
            return course


def add_enrollment(student_id, course_id, is_active=True, mode='honor'):
    """Append an enrollment to the enrollments array."""
    enrollment = {
        "created": datetime.datetime.now(),
        "mode": mode,
        "is_active": is_active,
        "course": _get_fake_course_info(course_id),
        "student": student_id
    }
    _ENROLLMENTS.append(enrollment)
    return enrollment


# pylint: disable=unused-argument
def add_or_update_enrollment_attr(user_id, course_id, attributes):
    """Add or update enrollment attribute array"""
    for attribute in attributes:
        _ENROLLMENT_ATTRIBUTES.append({
            'namespace': attribute['namespace'],
            'name': attribute['name'],
            'value': attribute['value']
        })


# pylint: disable=unused-argument
def get_enrollment_attributes(user_id, course_id):
    """Retrieve enrollment attribute array"""
    return _ENROLLMENT_ATTRIBUTES


def set_expired_mode(course_id):
    """Set course verified mode as expired."""
    _VERIFIED_MODE_EXPIRED.append(course_id)


def add_course(course_id, enrollment_start=None, enrollment_end=None, invite_only=False, course_modes=None):
    """Append course to the courses array."""
    course_info = {
        "course_id": course_id,
        "enrollment_end": enrollment_end,
        "course_modes": [],
        "enrollment_start": enrollment_start,
        "invite_only": invite_only,
    }
    if not course_modes:
        course_info['course_modes'].append(_DEFAULT_FAKE_MODE)
    else:
        for mode in course_modes:
            new_mode = copy.deepcopy(_DEFAULT_FAKE_MODE)
            new_mode['slug'] = mode
            course_info['course_modes'].append(new_mode)
    _COURSES.append(course_info)


def reset():
    """Set the enrollments and courses arrays to be empty."""
    global _COURSES  # pylint: disable=global-statement
    _COURSES = []
    global _ENROLLMENTS  # pylint: disable=global-statement
    _ENROLLMENTS = []
    global _VERIFIED_MODE_EXPIRED  # pylint: disable=global-statement
    _VERIFIED_MODE_EXPIRED = []
