from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb
from datetime import date
import re
import os
import sys
  
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/upload/photos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

  
mysql = MySQL(app)



  
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        # Get user role from the session
        user_role = session.get('User_Type')

        # Render different content based on user role
        if user_role == 'Admin':
            return render_template('dashboard.html', user_role='Admin')
        elif user_role == 'Teacher':
            return render_template('dashboard.html', user_role='Teacher')
        elif user_role == 'Student':
            return render_template('dashboard.html', user_role='Student')
    return redirect(url_for('Admin_login'))



@app.route('/Admin_login', methods=['GET', 'POST'])
def Admin_login():
    if request.method == "POST" and 'User_name' in request.form and 'user_Password' in request.form:
        Username = request.form['User_name']
        passw = request.form['user_Password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_name = %s AND user_Password = %s", (Username, passw))
        Admin = cur.fetchone()
        cur.close()
        
        if Admin:
            if Admin[4] == 'Admin':  # Assuming user_role is the 5th column
                session['loggedin'] = True
                session['User_ID'] = Admin[0]
                session['User_name'] = Admin[1]
                session['user_email'] = Admin[2]
                session['User_Type'] = 'Admin'  # Set user type in session
                
                return redirect(url_for('dashboard'))      
            else:
                flash("Only Admin can login")
        else:
            flash("Incorrect email or password")
    return render_template('Admin_login.html')

########################### Student Login Section ##################################

@app.route('/Student_login', methods=['GET', 'POST'])
def Student_login():
    if request.method == 'POST' and 'User_name' in request.form and 'user_Password' in request.form:
        Username = request.form['User_name']
        passw = request.form['user_Password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_name = %s AND user_Password = %s", (Username, passw))
        student = cur.fetchone()
        cur.close()
        
        if student:
            if student[4] == 'Student':  # Assuming 'user_role' is the 5th column
                session['loggedin'] = True
                session['User_ID'] = student[0]  # Assuming 'user_id' is the 1st column
                session['User_name'] = student[1]  # Assuming 'user_name' is the 2nd column
                session['user_email'] = student[2]  # Assuming 'user_email' is the 3rd column
                session['User_Type'] = 'Student'  # Store the role in the session
                
                return redirect(url_for('dashboard'))
            else:
                flash("Only Students can log in.", 'danger')
        else:
            flash("Incorrect username or password.", 'danger')
    
    return render_template('Student_login.html')


########################### Teacher Login Section ##################################

@app.route('/Teacher_login', methods=['GET', 'POST'])
def Teacher_login():
    if request.method == 'POST' and 'User_name' in request.form and 'user_Password' in request.form:
        Username = request.form['User_name']
        passw = request.form['user_Password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_name = %s AND user_Password = %s", (Username, passw))
        Teacher = cur.fetchone()
        cur.close()
        
        if Teacher:
            if Teacher[4] == 'Teacher':  # Assuming 'user_role' is the 5th column
                session['loggedin'] = True
                session['User_ID'] = Teacher[0]  # Assuming 'user_id' is the 1st column
                session['User_name'] = Teacher[1]  # Assuming 'user_name' is the 2nd column
                session['user_email'] = Teacher[2]  # Assuming 'user_email' is the 3rd column
                session['User_Type'] = 'Teacher'  # Store the role in the session

                return redirect(url_for('dashboard'))
            else:
                flash("Only Teachers can log in.", 'danger')
        else:
            flash("Incorrect username or password.", 'danger')
    
    return render_template('Teacher_login.html')


@app.route('/logout')
def logout():
    if 'loggedin' in session:  # Check if the user is logged in
        user_type = session.get('User_Type')
        
        # Clear the session data
        session.clear()
        flash("Logged out successfully to Back Log in.", 'success')
        
        # Redirect based on user type
        if user_type == 'Admin':
            return redirect(url_for('Admin_login'))
        elif user_type == 'Student':
            return redirect(url_for('Student_login'))
        elif user_type == 'Teacher':
            return redirect(url_for('Teacher_login'))
    
    return redirect(url_for('Admin_login'))  # Redirect to Admin login by default






if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run()
    os.execv(__file__, sys.argv)