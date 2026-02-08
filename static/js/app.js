// Global state
let courses = [];
let currentSchedule = null;
let totalSchedules = 0;
let currentScheduleIndex = 0;

// Time slots configuration
const TIME_SLOTS = [
    "08:30", "09:30", "10:30", "11:30", "12:50",
    "13:50", "14:50", "15:50", "16:50", "17:50",
    "18:50", "19:50", "20:50", "21:50"
];

const TIME_MAPPING = {
    "08:30": 0, "09:30": 1, "10:30": 2, "11:30": 3,
    "12:20": 4, "12:50": 4, "13:50": 5, "14:50": 6,
    "15:50": 7, "16:50": 8, "17:50": 9, "18:50": 10,
    "19:50": 11, "20:50": 12, "21:50": 13
};

const DAY_MAPPING = {
    'יום ראשון': 0,
    'יום שני': 1,
    'יום שלישי': 2,
    'יום רביעי': 3,
    'יום חמישי': 4,
    'יום שישי': 5
};

const COLORS = [
    'color-0', 'color-1', 'color-2', 'color-3', 'color-4',
    'color-5', 'color-6', 'color-7', 'color-8', 'color-9'
];

// Initialize
// Assuming loadCourses() is a function that needs to be defined elsewhere or is a placeholder.
// For now, it's added as per instruction.
// loadCourses(); // This line was in the instruction but not in the original file. Keeping it commented as it's not defined.

// Lesson Selection Modal Logic
let currentCourseData = null;
let selectedLessons = {};

function showLessonSelectionModal(courseData) {
    currentCourseData = courseData;
    selectedLessons = {};

    const modal = document.getElementById('lessonModal');
    const modalCourseName = document.getElementById('modalCourseName');
    const lessonOptions = document.getElementById('lessonOptions');

    modalCourseName.textContent = courseData.name;

    // Build lesson options HTML
    let html = '';

    // Check if there are multiple options for any lesson type
    const hasMultipleLectures = courseData.lesson_options.lectures.length > 1;
    const hasMultipleLabs = courseData.lesson_options.labs.length > 1;
    const hasMultiplePractices = courseData.lesson_options.practices.length > 1;

    // Only show modal if there are multiple options
    if (!hasMultipleLectures && !hasMultipleLabs && !hasMultiplePractices) {
        return false; // Don't show modal
    }

    // Lectures
    if (courseData.lesson_options.lectures.length > 0) {
        html += '<div class="lesson-type-section">';
        html += '<h4>הרצאות</h4>';
        courseData.lesson_options.lectures.forEach((lesson, idx) => {
            const isOnlyOption = courseData.lesson_options.lectures.length === 1;
            html += `
                <div class="lesson-option ${isOnlyOption ? 'selected' : ''}" 
                     data-type="lecture" 
                     data-index="${idx}"
                     ${isOnlyOption ? 'style="pointer-events: none;"' : ''}>
                    <div class="lesson-info">
                        <div class="lesson-time">${lesson.day} ${lesson.start}-${lesson.finish}</div>
                        <div class="lesson-lecturer">${lesson.lecturer}</div>
                    </div>
                </div>
            `;
            if (isOnlyOption) selectedLessons.lecture = idx;
        });
        html += '</div>';
    }

    // Labs
    if (courseData.lesson_options.labs.length > 0) {
        html += '<div class="lesson-type-section">';
        html += '<h4>מעבדות</h4>';
        courseData.lesson_options.labs.forEach((lesson, idx) => {
            const isOnlyOption = courseData.lesson_options.labs.length === 1;
            html += `
                <div class="lesson-option ${isOnlyOption ? 'selected' : ''}" 
                     data-type="lab" 
                     data-index="${idx}"
                     ${isOnlyOption ? 'style="pointer-events: none;"' : ''}>
                    <div class="lesson-info">
                        <div class="lesson-time">${lesson.day} ${lesson.start}-${lesson.finish}</div>
                        <div class="lesson-lecturer">${lesson.lecturer}</div>
                    </div>
                </div>
            `;
            if (isOnlyOption) selectedLessons.lab = idx;
        });
        html += '</div>';
    }

    // Practices
    if (courseData.lesson_options.practices.length > 0) {
        html += '<div class="lesson-type-section">';
        html += '<h4>תרגילים</h4>';
        courseData.lesson_options.practices.forEach((lesson, idx) => {
            const isOnlyOption = courseData.lesson_options.practices.length === 1;
            html += `
                <div class="lesson-option ${isOnlyOption ? 'selected' : ''}" 
                     data-type="practice" 
                     data-index="${idx}"
                     ${isOnlyOption ? 'style="pointer-events: none;"' : ''}>
                    <div class="lesson-info">
                        <div class="lesson-time">${lesson.day} ${lesson.start}-${lesson.finish}</div>
                        <div class="lesson-lecturer">${lesson.lecturer}</div>
                    </div>
                </div>
            `;
            if (isOnlyOption) selectedLessons.practice = idx;
        });
        html += '</div>';
    }

    lessonOptions.innerHTML = html;

    // Add click handlers to lesson options
    document.querySelectorAll('.lesson-option').forEach(option => {
        option.addEventListener('click', function () {
            const type = this.dataset.type;
            const index = parseInt(this.dataset.index);

            // Deselect other options of the same type
            document.querySelectorAll(`.lesson-option[data-type="${type}"]`).forEach(opt => {
                opt.classList.remove('selected');
            });

            // Select this option
            this.classList.add('selected');
            selectedLessons[type] = index;
        });
    });

    modal.style.display = 'block';
    return true;
}

function closeModal() {
    document.getElementById('lessonModal').style.display = 'none';
    currentCourseData = null;
    selectedLessons = {};
}

// Modal event listeners
document.getElementById('closeModal').addEventListener('click', closeModal);
document.getElementById('cancelSelection').addEventListener('click', closeModal);

document.getElementById('confirmSelection').addEventListener('click', () => {
    // For now, just close the modal
    // In a full implementation, you would send the selected lessons to the backend
    // and regenerate the schedule with only those lessons
    console.log('Selected lessons:', selectedLessons);
    console.log('Course:', currentCourseData);
    closeModal();
    alert('בחירת שיעורים נשמרה! (תכונה זו תושלם בגרסה הבאה)');
});

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('lessonModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeScheduleGrid();
    loadSchedule();
});

// Initialize empty schedule grid
function initializeScheduleGrid() {
    const grid = document.getElementById('scheduleGrid');

    // Create time slots and cells
    TIME_SLOTS.forEach(time => {
        // Time label
        const timeLabel = document.createElement('div');
        timeLabel.className = 'time-label';
        timeLabel.textContent = time;
        grid.appendChild(timeLabel);

        // 6 day cells
        for (let day = 0; day < 6; day++) {
            const cell = document.createElement('div');
            cell.className = 'schedule-cell';
            cell.dataset.time = time;
            cell.dataset.day = day;
            grid.appendChild(cell);
        }
    });
}

// Add course
async function addCourse() {
    const input = document.getElementById('courseInput');
    const courseId = input.value.trim();
    const addButton = document.getElementById('addButton');
    const errorMessage = document.getElementById('errorMessage');

    // Clear previous error
    errorMessage.textContent = '';
    input.classList.remove('error');

    if (!courseId) {
        alert('אנא הכנס מספר קורס');
        return;
    }

    // Show loading state
    addButton.disabled = true;
    addButton.textContent = 'טוען...';

    try {
        const response = await fetch('/api/courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ course_id: parseInt(courseId) }), // Ensure course_id is an integer
        });

        const data = await response.json();
        console.log('Add course response:', data); // Debug logging

        if (!response.ok) {
            throw new Error(data.error || 'שגיאה בהוספת קורס');
        }

        // Ensure we have course data
        if (!data.course) {
            throw new Error('לא התקבל מידע על הקורס');
        }

        // Add to courses list
        courses.push(data.course);
        console.log('Current courses:', courses); // Debug logging

        // Update UI
        updateCourseList();

        // Check if we should show lesson selection modal
        const hasMultipleOptions =
            data.course.lesson_options.lectures.length > 1 ||
            data.course.lesson_options.labs.length > 1 ||
            data.course.lesson_options.practices.length > 1;

        if (hasMultipleOptions) {
            // Show modal for lesson selection
            showLessonSelectionModal(data.course);
        }

        // Update schedule even if it's null (will clear if needed)
        updateSchedule(data.schedule || null);

        // Update schedule navigation
        totalSchedules = data.total_schedules || 1;
        currentScheduleIndex = data.current_index || 0;
        updateScheduleNav();

        // Clear input
        input.value = '';

    } catch (error) {
        console.error('Error adding course:', error); // Debug logging
        alert(`שגיאה: ${error.message}`);
    } finally {
        addButton.disabled = false;
        addButton.textContent = 'הוסף';
    }
}

// Remove course
async function removeCourse(courseId) {
    try {
        const response = await fetch(`/api/courses/${courseId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'שגיאה בהסרת קורס');
        }

        // Remove from courses list
        courses = courses.filter(c => c.id !== courseId);

        // Update UI
        updateCourseList();
        updateSchedule(data.schedule);

        // Update schedule navigation
        totalSchedules = data.total_schedules || 0;
        currentScheduleIndex = data.current_index || 0;
        updateScheduleNav();

    } catch (error) {
        showError(error.message);
    }
}

// Load current schedule
async function loadSchedule() {
    try {
        const response = await fetch('/api/schedule');
        const data = await response.json();

        courses = data.courses || [];
        updateCourseList();
        updateSchedule(data.schedule);

        // Update schedule navigation
        totalSchedules = data.total_schedules || 0;
        currentScheduleIndex = data.current_index || 0;
        updateScheduleNav();

    } catch (error) {
        console.error('Error loading schedule:', error);
    }
}

// Update course list display
function updateCourseList() {
    const courseList = document.getElementById('courseList');

    if (courses.length === 0) {
        courseList.innerHTML = '<p class="empty-message">טרם נוספו קורסים</p>';
        return;
    }

    courseList.innerHTML = courses.map((course, index) => {
        const colorClass = COLORS[index % COLORS.length];
        return `
            <div class="course-item ${colorClass}">
                <div class="course-info">
                    <div class="course-name">${course.id} - ${course.name}</div>
                    <div class="course-details">${course.points} נ"ז</div>
                </div>
                <button class="remove-btn" onclick="removeCourse(${course.id})">הסר</button>
            </div>
        `;
    }).join('');
}

// Update schedule grid
function updateSchedule(schedule) {
    console.log('updateSchedule called with:', schedule); // Debug
    console.log('Schedule type:', typeof schedule); // Debug
    console.log('Schedule is array:', Array.isArray(schedule)); // Debug
    console.log('Schedule length:', schedule ? schedule.length : 'null'); // Debug

    // Clear all cells
    clearSchedule();

    if (!schedule || schedule.length === 0) {
        console.log('No schedule data to display'); // Debug
        return;
    }

    currentSchedule = schedule;

    // Group lessons by course
    const courseMap = new Map();
    schedule.forEach(lesson => {
        console.log('Processing lesson:', lesson); // Debug
        if (!courseMap.has(lesson.course_id)) {
            courseMap.set(lesson.course_id, []);
        }
        courseMap.get(lesson.course_id).push(lesson);
    });

    // Assign colors to courses
    const courseIds = Array.from(courseMap.keys());

    // Fill schedule cells
    schedule.forEach(lesson => {
        const dayIndex = DAY_MAPPING[lesson.day];
        const startIndex = TIME_MAPPING[lesson.start];
        const finishIndex = TIME_MAPPING[lesson.finish];

        if (dayIndex === undefined || startIndex === undefined || finishIndex === undefined) {
            return;
        }

        const courseIndex = courseIds.indexOf(lesson.course_id);
        const colorClass = COLORS[courseIndex % COLORS.length];

        // Fill cells for lesson duration
        for (let timeIdx = startIndex; timeIdx < finishIndex; timeIdx++) {
            const time = TIME_SLOTS[timeIdx];
            const cell = document.querySelector(
                `.schedule-cell[data-time="${time}"][data-day="${dayIndex}"]`
            );

            if (cell) {
                // Abbreviate course name if too long
                let courseName = lesson.course_name;
                if (courseName.length > 15) {
                    courseName = courseName.substring(0, 12) + '...';
                }

                // Build HTML with lecturer if available
                let html = `
                    <div class="lesson-info">
                        <div class="lesson-course">${courseName}</div>
                        <div class="lesson-type">${lesson.type}</div>
                `;

                if (lesson.lecturer && lesson.lecturer.trim()) {
                    html += `<div class="lesson-lecturer">${lesson.lecturer}</div>`;
                }

                html += `</div>`;

                cell.innerHTML = html;
                cell.classList.add('filled', colorClass);
            }
        }
    });
}

// Clear schedule grid
function clearSchedule() {
    const cells = document.querySelectorAll('.schedule-cell');
    cells.forEach(cell => {
        cell.innerHTML = '';
        cell.className = 'schedule-cell';
    });
}

// Show error message
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const input = document.getElementById('courseInput');

    errorMessage.textContent = message;
    input.classList.add('error');

    // Clear after 3 seconds
    setTimeout(() => {
        errorMessage.textContent = '';
        input.classList.remove('error');
    }, 3000);
}

// Navigate between schedules
async function navigateSchedule(direction) {
    try {
        const response = await fetch(`/api/schedule/navigate/${direction}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'שגיאה בניווט');
        }

        // Update schedule display
        updateSchedule(data.schedule);
        currentScheduleIndex = data.current_index;
        totalSchedules = data.total_schedules;
        updateScheduleNav();

    } catch (error) {
        console.error('Navigation error:', error);
    }
}

// Update schedule navigation UI
function updateScheduleNav() {
    const navElement = document.getElementById('scheduleNav');
    const currentIndexElement = document.getElementById('currentIndex');
    const totalSchedulesElement = document.getElementById('totalSchedules');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (totalSchedules > 1) {
        navElement.style.display = 'flex';
        currentIndexElement.textContent = currentScheduleIndex + 1;
        totalSchedulesElement.textContent = totalSchedules;

        // Enable/disable buttons
        prevBtn.disabled = currentScheduleIndex === 0;
        nextBtn.disabled = currentScheduleIndex === totalSchedules - 1;
    } else {
        navElement.style.display = 'none';
    }
}
