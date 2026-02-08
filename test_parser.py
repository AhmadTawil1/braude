import sys
sys.path.insert(0, 'brauler')

from course import Course

print("=" * 60)
print("Testing Course Data Parser")
print("=" * 60)

course_id = 61954
print(f"\nFetching course {course_id}...")

try:
    course = Course(course_id)
    
    print(f"\n✅ Course found: {course.name}")
    print(f"Points: {course.points}")
    print(f"Lectures: {len(course.lectures)}")
    print(f"Labs: {len(course.labs)}")
    print(f"Practices: {len(course.practices)}")
    
    all_lessons = course.lectures + course.labs + course.practices
    print(f"Total lessons: {len(all_lessons)}")
    
    if all_lessons:
        print("\nFirst few lessons:")
        for i, lesson in enumerate(all_lessons[:5]):
            print(f"  {i+1}. {lesson.type} - {lesson.day} {lesson.start}-{lesson.finish} ({lesson.lecturer})")
    else:
        print("\n❌ No lessons found!")
        print("\nThis means the parser couldn't extract lesson data from the website.")
        print("The Braude website structure may have changed.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
