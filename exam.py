########################### EXAM SECTION ##################################

@app.route("/exams", methods=['GET', 'POST'])
def exams():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # LEFT JOIN to get the subject name for each exam
        
        cursor.execute('''
            SELECT e.id, e.exam_name, e.exam_date,  s.subject 
            FROM sms_exams e 
            LEFT JOIN sms_subjects s ON s.subject_id = e.subject_id
        ''')
        exams = cursor.fetchall()

        cursor.execute('SELECT * FROM sms_subjects')
        subjects = cursor.fetchall()
        return render_template("exam.html", exams=exams, subjects=subjects)
    return redirect(url_for('login'))



@app.route("/save_exam", methods=['GET', 'POST'])
def save_exam():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'exam_name' in request.form and 'exam_date' in request.form and 'subject_id' in request.form:
            exam_name = request.form['exam_name']
            exam_date = request.form['exam_date']
            subject_id = request.form['subject_id']
            action = request.form['action']
            exam_id = request.form.get('examid')  # Get the exam_id if present

            if action == 'updateExam' and exam_id:
                cursor.execute('''
                    UPDATE sms_exams 
                    SET exam_name = %s, exam_date = %s, subject_id = %s 
                    WHERE id = %s
                ''', (exam_name, exam_date, subject_id, exam_id))
                mysql.connection.commit()
                flash("Exam updated successfully!", "success")
            else:
                cursor.execute('''
                    INSERT INTO sms_exams (exam_name, exam_date, subject_id) 
                    VALUES (%s, %s, %s)
                ''', (exam_name, exam_date, subject_id))
                mysql.connection.commit()
                flash("Exam added successfully!", "success")

            return redirect(url_for('exams'))
        else:
            flash('Please fill out all form fields.', 'danger')

        return redirect(url_for('exams'))
    return redirect(url_for('login'))


@app.route("/delete_exam", methods=['GET'])
def delete_exam():
    if 'loggedin' in session:
        exam_id = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_exams WHERE id = %s', (exam_id,))
        mysql.connection.commit()
        flash('Exam record deleted successfully!', 'danger')
        return redirect(url_for('exams'))
    return redirect(url_for('login'))