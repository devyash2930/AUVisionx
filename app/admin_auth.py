import firebase_admin
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.firebase_config import firebase_app
from firebase_admin import auth, db
from flask import session

ref_students = db.reference("/students")
ref_admin = db.reference("/admin")

auth_bp = Blueprint('auth', __name__)

# Sample user class
class User:
    def __init__(self, user_id, is_admin=False):
        self.id = user_id
        self.is_admin = is_admin

# Sample Firebase authentication logic
def firebase_authenticate(email, password):
    # You can implement actual Firebase authentication logic here if needed
    return

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check student data
    student_data = ref_students.get()
    if student_data:
        for key, value in student_data.items():
            if value.get('student_email') == email and value.get('student_password') == password:
                user_l = key
                session['user_l'] = user_l
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
    print("noooooooo")
    # If no student match, check admin data
    admin_data = ref_admin.get()
    print("admin", admin_data)
    if admin_data:
        stored_email = admin_data.get('admin_email')
        stored_password = admin_data.get('admin_password')
        print(stored_email, stored_password, email, password)
        if email == stored_email and password == stored_password:
            # Set the user_id in the session
            user_id = 'admin'
            session['user_id'] = user_id

            # Flash a success message and redirect to the admin dashboard
            flash('Login successful!', 'success')
            return redirect(url_for('admin_functions'))

    # If no matching user or admin is found, flash an error message
    flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    # Clear the user session
    session.clear()

    # Optionally, you can add a flash message to indicate successful logout
    flash('Logged out successfully!', 'success')

    # Redirect to the login page or any other desired page after logout
    return redirect(url_for('auth.login'))
