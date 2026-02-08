"""Quick test to debug scheduler"""
import sys
sys.path.insert(0, 'brauler')

from course import Course
from scheduler import scheduler, find_non_overlapping_lessons

course = Course(61954)
print(f"Course: {course.name}")
print(f"Lectures: {len(course.lectures)}")
print(f"Labs: {len(course.labs)}")  
print(f"Practices: {len(course.practices)}")
print()

# Test find_non_overlapping_lessons
print("Finding non-overlapping lessons...")
count = 0
for lessons in find_non_overlapping_lessons(course, 1, 1, 1):
    count += 1
    print(f"Combination {count}:")
    for lesson in lessons:
        print(f"  {lesson.type} - {lesson.day} {lesson.start}-{lesson.finish}")
    if count >= 3:  # Only show first 3
        break

print(f"\nTotal combinations found: {count}")

# Test full scheduler
print("\nTesting full scheduler...")
schedule, latest = scheduler([course])
print(f"Schedule: {schedule}")
print(f"Latest: {latest}")
