"""Debug GUI schedule display"""
import sys
sys.path.insert(0, 'brauler')

from course import Course
from scheduler import scheduler

course = Course(61954)
print(f"Course: {course.name}")
print(f"\nLessons:")
for lecture in course.lectures:
    print(f"  Lecture: day='{lecture.day}' start={lecture.start} finish={lecture.finish}")
for lab in course.labs:
    print(f"  Lab: day='{lab.day}' start={lab.start} finish={lab.finish}")

schedule, latest = scheduler([course])
print(f"\nSchedule generated: {schedule is not None}")
print(f"Latest time: {latest}")

if schedule:
    print("\nSchedule details:")
    for course_obj, lessons in schedule:
        print(f"  Course: {course_obj.name}")
        for lesson in lessons:
            print(f"    {lesson.type} - {lesson.day} {lesson.start}-{lesson.finish}")

# Test day mapping
print("\n\nDay mapping test:")
days = {
    'יום ראשון': 0,    # Sunday
    'יום שני': 1,      # Monday  
    'יום שלישי': 2,    # Tuesday
    'יום רביעי': 3,    # Wednesday
    'יום חמישי': 4,    # Thursday
    'יום שישי': 5      # Friday
}
for lecture in course.lectures:
    day_index = days.get(lecture.day)
    print(f"  Lecture day '{lecture.day}' -> index: {day_index}")
for lab in course.labs:
    day_index = days.get(lab.day)
    print(f"  Lab day '{lab.day}' -> index: {day_index}")
