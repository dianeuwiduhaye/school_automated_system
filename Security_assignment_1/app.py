# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Uwidu/Desktop/Security assignment 1/instance/database.db'


db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Add a 'role' field to distinguish user types

class StudentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)

class FacilitatorFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_text = db.Column(db.String(255), nullable=False)

class TeamLeadTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.String(255), nullable=False)

# Routes and views

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role'] #Get the selected role from the form

        # Check if the password meets your strength criteria here
        password_strength = 0

        # Check if the password contains at least 8 characters
        if len(password) >= 8:
            password_strength += 1

        # Check if the password contains at least one lowercase letter
        if any(c.islower() for c in password):
            password_strength += 1

        # Check if the password contains at least one uppercase letter
        if any(c.isupper() for c in password):
            password_strength += 1

        # Check if the password contains at least one number
        if any(c.isdigit() for c in password):
            password_strength += 1

        # Check if the password contains at least one special character
        if any(not c.isalnum() for c in password):
            password_strength += 1

        # Define password strength levels
        strength_levels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
        strength_colors = ['#FF0000', '#FF9900', '#FFFF00', '#99FF00', '#00FF00']

        # Calculate the strength index
        strength_index = min(password_strength, 4)

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif strength_index < 2:
            flash('Password is too weak', 'danger')
        else:
            # Hash the password before storing it in the database
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password, role=role)  # Assign a role
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'facilitator':
                return redirect(url_for('facilitator_dashboard'))
            elif user.role == 'team_lead':
                return redirect(url_for('team_lead_dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        student_requests = StudentRequest.query.filter_by(student_id=user.id).all()
        
        return render_template('student_dashboard.html', user=user, requests=student_requests)
    else:
        return redirect(url_for('login'))

@app.route('/facilitator_dashboard')
def facilitator_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        facilitator_feedbacks = FacilitatorFeedback.query.filter_by(facilitator_id=user.id).all()
        
        return render_template('facilitator_dashboard.html', user=user, feedbacks=facilitator_feedbacks)
    else:
        return redirect(url_for('login'))

@app.route('/team_lead_dashboard')
def team_lead_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        team_lead_tasks = TeamLeadTask.query.all()
        
        return render_template('team_lead_dashboard.html', user=user, tasks=team_lead_tasks)
    else:
        return redirect(url_for('login'))

@app.route('/submit_request', methods=['POST'])
def submit_request():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        if user.role == 'student':
            request_content = request.form['request_content']
            new_request = StudentRequest(student_id=user.id, content=request_content)
            db.session.add(new_request)
            db.session.commit()
            flash('Request submitted successfully!', 'success')
        elif user.role == 'facilitator':
            feedback_text = request.form['feedback_text']
            new_feedback = FacilitatorFeedback(facilitator_id=user.id, feedback_text=feedback_text)
            db.session.add(new_feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')
        elif user.role == 'team_lead':
            task_description = request.form['task_description']
            new_task = TeamLeadTask(task_description=task_description)
            db.session.add(new_task)
            db.session.commit()
            flash('Task submitted successfully!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

