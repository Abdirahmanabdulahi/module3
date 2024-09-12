################################  Result Exams ############################

@app.route("/results", methods=['GET', 'POST'])
def results():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT r.id, r.student_id, r.class_id, r.section_id, r.exam_id, s.subject, r.marks, e.exam_name 
            FROM sms_exam_results r
            LEFT JOIN sms_exams e ON r.exam_id = e.id
            LEFT JOIN sms_subjects s ON r.subject_id = s.subject_id
        ''')
        results = cursor.fetchall()

        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()

        cursor.execute('SELECT * FROM sms_subjects')
        subjects = cursor.fetchall()

        return render_template("exam_result.html", results=results, classes=classes, subjects=subjects)
    return redirect(url_for('login'))



@app.route("/save_result", methods=['GET', 'POST'])
def save_result():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'exam_name' in request.form and 'class_id' in request.form and 'subject_id' in request.form:
            exam_name = request.form['exam_name']
            class_id = request.form['class_id']
            subject_id = request.form['subject_id']
            action = request.form['action']

            if action == 'updateExam':
                exam_id = request.form['exam_id']
                cursor.execute('''
                    UPDATE sms_exam_results
                    SET exam_name = %s, class_id = %s, subject_id = %s 
                    WHERE id = %s
                ''', (exam_name, class_id, subject_id, exam_id))
                mysql.connection.commit()
            else:
                cursor.execute('''
                    INSERT INTO sms_exam_results (exam_name, class_id, subject_id) 
                    VALUES (%s, %s, %s)
                ''', (exam_name, class_id, subject_id))
                mysql.connection.commit()
            return redirect(url_for('results'))
        else:
            flash('Please fill out the form fields!', 'warning')
        return redirect(url_for('results'))
    return redirect(url_for('login'))



################  Add Exam_Result ###############

def calculate_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 80:
        return 'B'
    elif marks >= 70:
        return 'C'
    elif marks >= 60:
        return 'D'
    elif marks >= 50:
        return 'E'
    else:
        return 'F'

@app.route('/add_result', methods=['GET', 'POST'])
def add_result():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Fetch students, subjects, classes, sections, and exams for the dropdowns
        cursor.execute('SELECT id, name FROM sms_students')
        students = cursor.fetchall()
        
        cursor.execute('SELECT subject_id, subject FROM sms_subjects')
        subjects = cursor.fetchall()
    
        cursor.execute('SELECT id, name FROM sms_classes')
        classes = cursor.fetchall()
    
        cursor.execute('SELECT section_id, section FROM sms_section')
        sections = cursor.fetchall()
        
        cursor.execute('SELECT id, exam_name FROM sms_exams')
        exams = cursor.fetchall()
        
        if request.method == 'POST':
            student_id = request.form.get('student_id')
            subject_id = request.form.get('subject_id')
            class_id = request.form.get('classid')
            section_id = request.form.get('sectionid')
            exam_id = request.form.get('exam_id')
            marks_str = request.form.get('marks')
    
            # Validate that all fields are filled
            if not all([student_id, subject_id, class_id, section_id, exam_id, marks_str]):
                flash("Please fill out all fields.", "warning")
                return render_template('Add_exam.html', students=students, sections=sections, subjects=subjects, classes=classes, exams=exams)
            
            # Convert marks from string to integer
            try:
                marks = int(marks_str)
            except ValueError:
                flash("Invalid marks input. Please enter a valid number.", "danger")
                return render_template('Add_exam.html', students=students, sections=sections, subjects=subjects, classes=classes, exams=exams)
            
            # Validate marks range
            if marks < 0 or marks > 100:
                flash("Marks must be between 0 and 100.", "danger")
                return render_template('Add_exam.html', students=students, sections=sections, subjects=subjects, classes=classes, exams=exams)
    
            # Calculate grade
            grade = calculate_grade(marks)
            
            # Determine status based on marks
            status = "Pass" if marks >= 50 else "Fail"
    
            try:
                # Insert the result into the database, including grade
                cursor.execute(
                    '''INSERT INTO sms_exam_results 
                    (student_id, subject_id, exam_id, class_id, section_id, marks, status, grade, exam_name) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
                    (SELECT exam_name FROM sms_exams WHERE id = %s))''',
                    (student_id, subject_id, exam_id, class_id, section_id, marks, status, grade, exam_id)
                )
                mysql.connection.commit()
                flash(" Yes Result added successfully!", "success")
                return redirect(url_for('results'))
            except MySQLdb.Error as e:
                mysql.connection.rollback()
                flash(f"An error occurred while adding the result: {e}", "danger")
        
    finally:
        cursor.close()
    
    return render_template('Add_exam.html', students=students, sections=sections, subjects=subjects, classes=classes, exams=exams)



################  Update Exam_Result ###############

@app.route('/update_result/<int:id>', methods=['GET', 'POST'])
def update_result(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Fetch the result to be updated
        cursor.execute('SELECT * FROM sms_exam_results WHERE id = %s', (id,))
        result = cursor.fetchone()

        if not result:
            flash('Result not found.', 'danger')
            return redirect(url_for('results'))

        # Fetch dropdown data for the form
        cursor.execute('SELECT id, name FROM sms_students')
        students = cursor.fetchall()

        cursor.execute('SELECT subject_id, subject FROM sms_subjects')
        subjects = cursor.fetchall()

        cursor.execute('SELECT id, name FROM sms_classes')
        classes = cursor.fetchall()

        cursor.execute('SELECT section_id, section FROM sms_section')
        sections = cursor.fetchall()

        cursor.execute('SELECT id, exam_name FROM sms_exams')
        exams = cursor.fetchall()

        if request.method == 'POST':
            student_id = request.form.get('student_id')
            subject_id = request.form.get('subject_id')
            class_id = request.form.get('classid')
            section_id = request.form.get('sectionid')
            exam_id = request.form.get('exam_id')
            marks_str = request.form.get('marks')

            # Validate that all fields are filled
            if not all([student_id, subject_id, class_id, section_id, exam_id, marks_str]):
                flash("Please fill out all fields.", "warning")
                return render_template('update_result.html', result=result, students=students, subjects=subjects, classes=classes, sections=sections, exams=exams)
            
            # Convert marks from string to integer
            try:
                marks = int(marks_str)
            except ValueError:
                flash("Invalid marks input. Please enter a valid number.", "danger")
                return render_template('update_result.html', result=result, students=students, subjects=subjects, classes=classes, sections=sections, exams=exams)
            
            # Validate marks range
            if marks < 0 or marks > 100:
                flash("Marks must be between 0 and 100.", "danger")
                return render_template('update_result.html', result=result, students=students, subjects=subjects, classes=classes, sections=sections, exams=exams)
    
            # Calculate grade
            grade = calculate_grade(marks)

            # Determine status based on marks
            status = "Pass" if marks >= 50 else "Fail"

            try:
                # Update the result in the database
                cursor.execute(
                    '''UPDATE sms_exam_results 
                    SET student_id=%s, subject_id=%s, exam_id=%s, class_id=%s, section_id=%s, marks=%s, status=%s, grade=%s 
                    WHERE id=%s''',
                    (student_id, subject_id, exam_id, class_id, section_id, marks, status, grade, id)
                )
                mysql.connection.commit()
                flash("Result updated successfully! waw", "success")
                return redirect(url_for('results'))
            except MySQLdb.Error as e:
                mysql.connection.rollback()
                flash(f"An error occurred while updating the result: {e}", "danger")
    
    finally:
        cursor.close()
    
    return render_template('update_result.html', result=result, students=students, subjects=subjects, classes=classes, sections=sections, exams=exams)








################  Delete Exam_Result ###############
@app.route("/delete_result", methods=['GET'])
def delete_result():
    if 'loggedin' in session:
        id = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_exam_results WHERE id = %s', (id,))
        mysql.connection.commit()
        return redirect(url_for('results'))
    return redirect(url_for('login'))

################  View  ###############
@app.route("/view_exam_results", methods=['GET'])
def view_exam_results():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_exam_results')
        attendance_records = cursor.fetchall()
        return render_template("exam_results_view.html", records=attendance_records)
    return redirect(url_for('login'))


################  View Exam_Result & Edit ###############
@app.route("/exam_results", methods =['GET', 'POST'])
def exam_results():
    if 'loggedin' in session:      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_exam_results')
        results = cursor.fetchall()          
        return render_template("exam_result.html", results = results)
    return redirect(url_for('login')) 
####################### View Exam Results STD ###########
@app.route("/exam_results_view", methods =['GET', 'POST'])
def exam_results_view():
    if 'loggedin' in session:      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_exam_results')
        results = cursor.fetchall()          
        return render_template("exam_resultSTD.html", results = results)
    return redirect(url_for('login')) 

    #################### End Result Section ###########################