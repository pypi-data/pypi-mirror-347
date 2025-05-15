from .courses import *

def total_duration():

    return sum(course.duration for course in course_list)
