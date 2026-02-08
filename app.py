from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sys
import os

# Add brauler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brauler'))

from course import Course
import scheduler
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
CORS(app)

# In-memory storage for courses (use session for multi-user support)
courses_store = {}

# In-memory cache for schedules (Course objects can't be serialized to session)
schedules_cache = {}

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/courses', methods=['POST'])
def add_course():
    """Add a course by ID"""
    try:
        data = request.get_json()
        course_id = int(data.get('course_id'))
        
        # Get or create session ID
        if 'session_id' not in session:
            import uuid
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Initialize courses list for this session
        if session_id not in courses_store:
            courses_store[session_id] = []
        
        # Check if course already added
        if any(c.id == course_id for c in courses_store[session_id]):
            return jsonify({
                'success': False,
                'error': 'קורס זה כבר נוסף'
            }), 400
        
        # Fetch course data
        course = Course(course_id)
        courses_store[session_id].append(course)
        
        # Check if course has any lessons
        total_lessons = len(course.lectures) + len(course.labs) + len(course.practices)
        
        if total_lessons == 0:
            # Course has no lessons - add it but don't regenerate schedule
            print(f"DEBUG: Course {course_id} has no lessons, skipping schedule generation")
            
            # Format lesson options (will be empty)
            def format_lesson_option(lesson):
                return {
                    'type': lesson.type,
                    'day': lesson.day,
                    'start': lesson.start,
                    'finish': lesson.finish,
                    'lecturer': lesson.lecturer
                }
            
            return jsonify({
                'success': True,
                'course': {
                    'id': course.id,
                    'name': course.name,
                    'points': course.points,
                    'lectures': 0,
                    'labs': 0,
                    'practices': 0,
                    'lesson_options': {
                        'lectures': [],
                        'labs': [],
                        'practices': []
                    }
                },
                'schedule': None,  # Don't change existing schedule
                'total_schedules': session.get('all_schedules_count', 0),
                'current_index': session.get('current_schedule_index', 0),
                'no_lessons': True  # Flag to indicate course has no lessons
            })
        
        # Always allow overlaps - use overlap-enabled scheduler
        all_schedules = list(scheduler.generate_schedules_with_overlaps(courses_store[session_id], 1, 1, 1))
        print(f"DEBUG: Generated {len(all_schedules)} total schedules")  # Debug
        
        # Filter valid schedules
        valid_schedules = [s for s in all_schedules if all(scheduler.has_required_lessons(c, l) for c, l in s)]
        print(f"DEBUG: {len(valid_schedules)} valid schedules after filtering")  # Debug
        
        # Convert to serializable format and store in session
        session['all_schedules_count'] = len(valid_schedules)
        session['current_schedule_index'] = 0
        
        # Get current schedule (keep as objects for formatting)
        schedule_data = valid_schedules[0] if valid_schedules else None
        print(f"DEBUG: schedule_data is {'None' if schedule_data is None else 'valid'}")  # Debug
        
        # Store schedules in memory (not in session) using session_id as key
        schedules_cache[session_id] = valid_schedules
        
        formatted_schedule = format_schedule(schedule_data) if schedule_data else None
        print(f"DEBUG: formatted_schedule has {len(formatted_schedule) if formatted_schedule else 0} lessons")  # Debug
        
        # Format lesson options for frontend
        def format_lesson_option(lesson):
            return {
                'type': lesson.type,
                'day': lesson.day,
                'start': lesson.start,
                'finish': lesson.finish,
                'lecturer': lesson.lecturer
            }
        
        return jsonify({
            'success': True,
            'course': {
                'id': course.id,
                'name': course.name,
                'points': course.points,
                'lectures': len(course.lectures),
                'labs': len(course.labs),
                'practices': len(course.practices),
                'lesson_options': {
                    'lectures': [format_lesson_option(l) for l in course.lectures],
                    'labs': [format_lesson_option(l) for l in course.labs],
                    'practices': [format_lesson_option(l) for l in course.practices]
                }
            },
            'schedule': formatted_schedule,
            'total_schedules': len(valid_schedules),
            'current_index': 0
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'שגיאה בטעינת קורס: {str(e)}'
        }), 500

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def remove_course(course_id):
    """Remove a course by ID"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in courses_store:
            return jsonify({
                'success': False,
                'error': 'לא נמצאו קורסים'
            }), 404
        
        # Find and remove course
        courses_store[session_id] = [
            c for c in courses_store[session_id] if c.id != course_id
        ]
        
        # Regenerate ALL schedules
        if courses_store[session_id]:
            all_schedules = list(scheduler.generate_schedules(courses_store[session_id], 1, 1, 1))
            valid_schedules = [s for s in all_schedules if all(scheduler.has_required_lessons(c, l) for c, l in s)]
            
            # Store in memory cache
            schedules_cache[session_id] = valid_schedules
            
            session['all_schedules_count'] = len(valid_schedules)
            session['current_schedule_index'] = 0
            schedule_data = valid_schedules[0] if valid_schedules else None
        else:
            if session_id in schedules_cache:
                del schedules_cache[session_id]
            session['all_schedules_count'] = 0
            session['current_schedule_index'] = 0
            schedule_data = None
        
        return jsonify({
            'success': True,
            'schedule': format_schedule(schedule_data) if schedule_data else None,
            'total_schedules': session.get('all_schedules_count', 0),
            'current_index': 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """Get current schedule"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in courses_store:
            return jsonify({
                'schedule': None,
                'courses': [],
                'total_schedules': 0,
                'current_index': 0
            })
        
        courses = courses_store[session_id]
        
        # Get schedules from cache
        all_schedules = schedules_cache.get(session_id, [])
        current_index = session.get('current_schedule_index', 0)
        
        schedule_data = all_schedules[current_index] if all_schedules and current_index < len(all_schedules) else None
        
        return jsonify({
            'schedule': format_schedule(schedule_data) if schedule_data else None,
            'courses': [{
                'id': c.id,
                'name': c.name,
                'points': c.points
            } for c in courses],
            'total_schedules': len(all_schedules),
            'current_index': current_index
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schedule/navigate/<direction>', methods=['POST'])
def navigate_schedule(direction):
    """Navigate to next or previous schedule"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'success': False, 'error': 'אין מזהה סשן'}), 404
        
        # Get schedules from cache
        all_schedules = schedules_cache.get(session_id, [])
        current_index = session.get('current_schedule_index', 0)
        
        if not all_schedules:
            return jsonify({'success': False, 'error': 'אין מערכות זמינות'}), 404
        
        # Update index
        if direction == 'next' and current_index < len(all_schedules) - 1:
            current_index += 1
        elif direction == 'prev' and current_index > 0:
            current_index -= 1
        
        session['current_schedule_index'] = current_index
        schedule_data = all_schedules[current_index]
        
        return jsonify({
            'success': True,
            'schedule': format_schedule(schedule_data),
            'current_index': current_index,
            'total_schedules': len(all_schedules)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def format_schedule(schedule_data):
    """Format schedule data for frontend"""
    if not schedule_data:
        return None
    
    formatted = []
    for course, lessons in schedule_data:
        for lesson in lessons:
            formatted.append({
                'course_id': course.id,
                'course_name': course.name,
                'type': lesson.type,
                'day': lesson.day,
                'start': lesson.start,
                'finish': lesson.finish,
                'lecturer': lesson.lecturer
            })
    
    return formatted

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
