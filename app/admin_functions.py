import firebase_admin
from firebase_admin import db
from flask import flash, redirect, render_template, request
from flask import Blueprint
from datetime import datetime


admin_functions_bp = Blueprint('admin_functions', __name__, url_prefix='/admin_functions')


def is_admin():
    # Implement the logic to check if the current user has admin privileges
    # This could involve checking the user's role or any other relevant criteria
    return True  # Placeholder, replace with actual implementation

@admin_functions_bp.route('/add_course', methods=['POST'])
def add_course():
    if is_admin():
        try:
            # Check if the course with the given course_id already exists
            courses_ref = db.reference('courses')
            course_id = request.form.get('course_id')
            existing_course = courses_ref.child(course_id).get()

            if existing_course:
                flash(f"Course with ID {course_id} already exists.", 'danger')
            else:
                # Add the new course
                course_data = {
                	'course_id' : request.form.get('course_id'),
                    'course_name': request.form.get('course_name'),
                    'course_capacity': int(request.form.get('course_capacity')),
                    'course_start_date': request.form.get('course_start_date'),
                    'course_end_date': request.form.get('course_end_date'),
                    'has_prerequisites': int(request.form.get('has_prerequisites')),
                }

                # Create a new key using the current timestamp for uniqueness
                new_course_key = f"course_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                courses_ref.child(new_course_key).set(course_data)
                
                flash(f"Course {course_id} added successfully.", 'success')
        except Exception as e:
            flash(f"Error adding course: {str(e)}", 'danger')
    else:
        flash("Unauthorized access. Admin privileges required.", 'danger')

    return redirect('/admin')




@admin_functions_bp.route('/delete_course', methods=['POST'])
def delete_course():
    if is_admin():
        try:
            # Get the course_id from the form data
            course_id = request.form.get('course_id')

            courses_ref = db.reference('courses')

            # Iterate through all courses to find and delete the matching one
            for key, course_data in courses_ref.get().items():
                if 'course_id' in course_data and course_data['course_id'] == course_id:
                    courses_ref.child(key).delete()
                    flash(f"Course {course_id} deleted successfully.", 'success')
                    break  # Exit the loop once the course is found and deleted
            else:
                flash(f"Course with ID {course_id} not found.", 'danger')

        except Exception as e:
            flash(f"Error deleting course: {str(e)}", 'danger')
    else:
        flash("Unauthorized access. Admin privileges required.", 'danger')

    return redirect('/admin')


@admin_functions_bp.route('/modify_course/<course_id>', methods=['GET', 'POST'])
def modify_course(course_id):
    if is_admin():
        try:
            courses_ref = db.reference('courses')
            course_ref = courses_ref.child(course_id)

            if course_ref.get():
                if request.method == 'POST':
                    # Get updated data from the form
                    updated_data = {
                        'course_name': request.form.get('course_name'),
                        'course_capacity': int(request.form.get('course_capacity')),
                        # Add other course properties as needed
                    }

                    course_ref.update(updated_data)
                    flash(f"Course {course_id} modified successfully.", 'success')

                return render_template('admin_functions/modify_course.html', course_id=course_id)

            else:
                flash(f"Course with ID {course_id} not found.", 'danger')

        except Exception as e:
            flash(f"Error modifying course: {str(e)}", 'danger')
    else:
        flash("Unauthorized access. Admin privileges required.", 'danger')

    return redirect('/admin')
