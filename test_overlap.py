"""Test if lecture and lab overlap"""
import sys
sys.path.insert(0, 'brauler')

from course import Course
from scheduler import do_lessons_overlap

course = Course(61954)
lecture = course.lectures[0]
lab = course.labs[0]

print(f"Lecture: {lecture.day} {lecture.start}-{lecture.finish}")
print(f"Lab: {lab.day} {lab.start}-{lab.finish}")
print(f"Do they overlap? {do_lessons_overlap(lecture, lab)}")
