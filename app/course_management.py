import firebase_admin
from firebase_admin import credentials, db
from flask import flash, session, render_template, redirect, url_for
from flask_login import current_user
from flask import Blueprint
from collections import defaultdict

course_management_bp = Blueprint('course_management', __name__)

# Initialize Firebase (replace 'path/to/your/firebase/credentials.json' with your actual path)
# cred = credentials.Certificate('path/to/your/firebase/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-database-url.firebaseio.com'})

# Function to enroll a student in a course
@course_management_bp.route('/enroll/<course_id>', methods=['POST'])
def enroll_in_course(course_id):
    student_id = session.get('user_l', None)

    if student_id is None:
        flash('User not logged in.', 'danger')
        return redirect(url_for('auth.login'))

    # Reference to the enrollment and courses nodes
    enrollment_ref = db.reference('/enrollments')
    courses_ref = db.reference('/courses')

    # Check if the student is already enrolled in the course
    if student_id is not None:
        enrollment_query = enrollment_ref.order_by_child('student_id').equal_to(student_id).get()

        if enrollment_query:
            already_enrolled = any(enrollment_data.get('course_id') == course_id for enrollment_data in enrollment_query.values())
            if already_enrolled:
                flash('Already enrolled in the course.', 'warning')
                return redirect(url_for('course_management.view_not_enrolled_courses'))

    # Check if the course has available seats
    course_info = courses_ref.child(course_id).get()
    if course_info and course_info.get('course_capacity', 0) > 0:
        # Enroll the student in the course
        new_enrollment_ref = enrollment_ref.push({
            'student_id': student_id,
            'course_id': course_id
        })

        # Update course capacity
        new_capacity = course_info['course_capacity'] - 1
        courses_ref.child(course_id).update({'course_capacity': new_capacity})

        flash('Enrollment successful!', 'success')
        return redirect(url_for('course_management.view_not_enrolled_courses'))
    else:
        flash('Course is full. Cannot enroll.', 'danger')
        return redirect(url_for('course_management.view_not_enrolled_courses'))



# View courses not currently enrolled
@course_management_bp.route('/courses/not-enrolled', methods=['GET'])
def view_not_enrolled_courses():
    student_id = session.get('user_l', None)  # Retrieve student ID from the session

    if not student_id:
        flash('User not logged in.', 'danger')
        return redirect(url_for('auth.login'))

    # Get all courses
    courses_ref = db.reference('/courses')
    all_courses = courses_ref.get()

    # Get enrolled courses
    enrollment_ref = db.reference('/enrollments')
    enrollments = enrollment_ref.order_by_child('student_id').equal_to(student_id).get()

    # Extract course IDs from enrollments
    enrolled_course_ids = [enrollment['course_id'] for enrollment in enrollments.values()]

    # Filter out enrolled courses
    not_enrolled_courses = {course_id: course for course_id, course in all_courses.items() if course_id not in enrolled_course_ids}

    # Pass not_enrolled_courses to the template along with additional fields
    return render_template('not_enrolled_courses.html', courses=not_enrolled_courses)


# View courses currently enrolled
@course_management_bp.route('/courses/enrolled', methods=['GET'])
def view_enrolled_courses():
    student_id = session.get('user_l', None)  # Retrieve student ID from the session

    if not student_id:
        flash('User not logged in.', 'danger')
        return redirect(url_for('auth.login'))

    # Get enrolled courses
    enrollment_ref = db.reference('/enrollments')
    enrollments = enrollment_ref.order_by_child('student_id').equal_to(student_id).get()

    # Get course details for enrolled courses
    enrolled_courses = {}
    courses_ref = db.reference('/courses')  # Moved this line outside the loop
    for enrollment in enrollments.values():
        course_id = enrollment['course_id']
        # Check if the course_id exists in the courses_ref
        if courses_ref.child(course_id).get():
            course_info = courses_ref.child(course_id).get()
            enrolled_courses[course_id] = course_info

    return render_template('enrolled_courses.html', courses=enrolled_courses)


# Function to drop a course

@course_management_bp.route('/drop_course/<course_id>', methods=['POST'])
def drop_course(course_id):
    student_id = session.get('user_l', None)

    if not student_id:
        flash('User not logged in.', 'danger')
        return redirect(url_for('auth.login'))

    # Reference to the enrollment node
    enrollment_ref = db.reference('/enrollments')

    # Find the enrollment node for the student and course
    enrollment_query = enrollment_ref.order_by_child('student_id').equal_to(student_id).get()

    # Check if the student is enrolled in the course
    if enrollment_query:
        for enrollment_key, enrollment_data in enrollment_query.items():
            if enrollment_data.get('course_id') == course_id:
                # Get the course capacity before deleting the enrollment
                course_ref = db.reference(f'/courses/{course_id}')
                course_info = course_ref.get()
                current_capacity = course_info.get('course_capacity', 0)

                # Remove the enrollment node
                enrollment_ref.child(enrollment_key).delete()

                # Update course capacity
                course_ref.update({'course_capacity': current_capacity + 1})

                # Flash a success message
                flash('Course dropped successfully!', 'success')
                break
        else:
            # Flash a warning if not enrolled in the selected course
            flash('Not enrolled in the selected course.', 'warning')
    else:
        # Flash a warning if not enrolled in any courses
        flash('Not enrolled in any courses.', 'warning')

    # Redirect back to the enrolled courses page
    return redirect(url_for('course_management.view_enrolled_courses'))

# ... (previous code)

# View all courses
@course_management_bp.route('/courses/all', methods=['GET'])
def view_all_courses():
    # Get all courses
    courses_ref = db.reference('/courses')
    all_courses = courses_ref.get()

    # Get professor information for each course
    professors_ref = db.reference('/faculty')
    all_professors = professors_ref.get()

    # Create a defaultdict to store professors for each course
    professors_by_course = defaultdict(list)

    # Iterate through faculty to add prof_name to each course
    for professor_id, professor_info in all_professors.items():
        if 'course_id' in professor_info and 'prof_name' in professor_info:
            course_id = professor_info['course_id']
            prof_name = professor_info['prof_name']
            # print(course_id, prof_name)
            professors_by_course[course_id].append(prof_name)
            print(professors_by_course)

    # Merge course information with professor information based on course_id
    for course_id, course_data in all_courses.items():
        # print(course_data["course_id"], "course_id")
        if course_data["course_id"] in professors_by_course:
            print(course_data['course_id'], professors_by_course[course_data["course_id"]])
            course_data['prof_name'] = professors_by_course[course_data["course_id"]]

    return render_template('all_courses.html', courses=all_courses)




