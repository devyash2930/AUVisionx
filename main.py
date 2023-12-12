# main.py
from flask import Flask, render_template, request
from flask_login import LoginManager
from app.auth import auth_bp
from app.course_management import course_management_bp
from app.admin_functions import admin_functions_bp
from app.firebase_config import firebase_app
import secrets
import subprocess


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Sample user loader function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(course_management_bp)
app.register_blueprint(admin_functions_bp)

# Routes to HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/run-command')
def run_command():
    # Retrieve the command from the query parameters
    command = request.args.get('command', '')

    try:
        # Execute the command using subprocess
        subprocess.run(command, shell=True, check=True)

        # Extract the port from the command (assuming it follows the pattern -p <port>)
        port_start_index = command.find('-p') + 3  # Assuming -p is followed by a space
        port_end_index = command.find(' ', port_start_index)
        port = int(command[port_start_index:port_end_index])

        # Redirect to the specified port
        return redirect(f'http://127.0.0.1:{port}')

    except subprocess.CalledProcessError as e:
        return f'Error executing command: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
