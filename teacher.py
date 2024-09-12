########################### Teacher Section ##################################

@app.route("/teacher", methods=['GET', 'POST'])
def teacher():
    if 'loggedin' in session:   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT t.teacher_id, t.teacher, s.subject FROM sms_teacher t LEFT JOIN sms_subjects s ON s.subject_id = t.subject_id')
        teachers = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_subjects')
        subjects = cursor.fetchall()  
        return render_template("teacher.html", teachers=teachers, subjects=subjects)
    return redirect(url_for('Admin_login'))

@app.route("/edit_teacher", methods=['GET'])
def edit_teacher():
    if 'loggedin' in session:
        teacher_id = request.args.get('teacher_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT t.teacher_id, t.teacher, t.subject_id FROM sms_teacher t WHERE t.teacher_id = %s', (teacher_id,))
        teachers = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_subjects')
        subjects = cursor.fetchall()
        
        return render_template("edit_teacher.html", teachers=teachers, subjects=subjects)
    return redirect(url_for('Admin_login'))

@app.route("/save_teacher", methods=['POST'])
def save_teacher():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'teacher_name' in request.form and 'specialization' in request.form:
            teacher_name = request.form['teacher_name']
            specialization = request.form['specialization']
            action = request.form['action']
            
            if action == 'updateTeacher':
                teacherid = request.form['teacherid']
                cursor.execute('UPDATE sms_teacher SET teacher=%s, subject_id=%s WHERE teacher_id=%s', (teacher_name, specialization, teacherid))
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO sms_teacher (teacher, subject_id) VALUES (%s, %s)', (teacher_name, specialization))
                mysql.connection.commit()
                flash("Teacher Added has been Successfully!","success")
            return redirect(url_for('teacher'))
        else:
            flash("Please fill out the form field!", "warninig")
        return redirect(url_for('teacher'))
    return redirect(url_for('Admin_login'))

@app.route("/delete_teacher", methods=['GET'])
def delete_teacher():
    if 'loggedin' in session:
        teacher_id = request.args.get('teacher_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_teacher WHERE teacher_id=%s', (teacher_id,))
        mysql.connection.commit()
        flash("Teacher Deleted has been Successfully", "danger")
        return redirect(url_for('teacher'))
    return redirect(url_for('Admin_login'))