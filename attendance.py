#################### Attendance Section ###########################

# Attendance page route
@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()
        
        return render_template("Att.html", classes=classes, sections=sections)
    return redirect(url_for('login'))





@app.route("/attendance_new", methods=['GET', 'POST'])
def attendance_new():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()

        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()

        if request.method == 'POST':
            classid = request.form['classid']
            sectionid = request.form['sectionid']
            
            # Validation for required fields
            if not classid or not sectionid:
                flash('Class and Section are required to load students!', 'danger')
                return redirect(url_for('attendance_new'))

            cursor.execute('''
                SELECT s.id, s.name, s.admission_no, s.roll_no 
                FROM sms_students s 
                WHERE s.class = %s AND s.section = %s
            ''', (classid, sectionid))
            students = cursor.fetchall()

            return render_template("attendance_new.html", classes=classes, sections=sections, students=students, classId=classid, sectionId=sectionid)
        
        return render_template("attendance_new.html", classes=classes, sections=sections)
    return redirect(url_for('login'))


@app.route("/saveAttendance", methods=['POST'])
def saveAttendance():
    if 'loggedin' in session:
        classid = request.form.get('classid')
        sectionid = request.form.get('sectionid')

        # Validate Class and Section
        if not classid or not sectionid:
            flash('Class and Section must be selected.', 'danger')
            return redirect(url_for('attendance_new'))

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Iterate through the students and save attendance
            for student_id in request.form:
                if student_id.startswith('attendance_'):
                    student_id = student_id.split('_')[1]
                    attendance_status = request.form.get(f'attendance_{student_id}')

                    # Insert or update attendance in the database
                    cursor.execute('''
                        INSERT INTO sms_attendance (student_id, class_id, section_id, attendance_status, attendance_date)
                        VALUES (%s, %s, %s, %s, CURDATE())
                        ON DUPLICATE KEY UPDATE attendance_status = %s
                    ''', (student_id, classid, sectionid, attendance_status, attendance_status))

            mysql.connection.commit()
            flash('Attendance saved successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error saving attendance: {str(e)}', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('attendance_new'))

    return redirect(url_for('login'))


@app.route("/update_attendance", methods=['GET', 'POST'])
def update_attendance():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':
            classid = request.form['classid']
            sectionid = request.form['sectionid']

            # Validate Class and Section
            if not classid or not sectionid:
                flash('Class and Section are required to view attendance.', 'danger')
                return redirect(url_for('update_attendance'))

            cursor.execute('''
                SELECT s.id, s.name, s.admission_no, s.roll_no, a.attendance_status 
                FROM sms_students s 
                LEFT JOIN sms_attendance a ON s.id = a.student_id AND a.attendance_date = CURDATE() 
                WHERE s.class = %s AND s.section = %s
            ''', (classid, sectionid))
            students = cursor.fetchall()

            cursor.execute('SELECT * FROM sms_classes')
            classes = cursor.fetchall()

            cursor.execute('SELECT * FROM sms_section')
            sections = cursor.fetchall()

            return render_template("update_attendance.html", classes=classes, sections=sections, students=students, classId=classid, sectionId=sectionid)

        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()

        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()

        return render_template("update_attendance.html", classes=classes, sections=sections)

    return redirect(url_for('login'))


@app.route("/save_updated_attendance", methods=['POST'])
def save_updated_attendance():
    if 'loggedin' in session:
        classid = request.form['classid']
        sectionid = request.form['sectionid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Iterate through the students and update attendance
        for student_id in request.form:
            if student_id.startswith('attendance_'):
                student_id = student_id.split('_')[1]
                attendance_status = request.form[f'attendance_{student_id}']
                
                # Update attendance in the database
                cursor.execute('''
                    UPDATE sms_attendance
                    SET attendance_status = %s
                    WHERE student_id = %s AND class_id = %s AND section_id = %s AND attendance_date = CURDATE()
                ''', (attendance_status, student_id, classid, sectionid))

        mysql.connection.commit()
        flash('Attendance updated successfully!', 'success')
        return redirect(url_for('update_attendance'))

    return redirect(url_for('login'))







@app.route("/view_attendance", methods=['GET'])
def view_attendance():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_attendance')
        attendance_records = cursor.fetchall()
        return render_template("view_attendance.html", records=attendance_records)
    return redirect(url_for('login'))