# ########################### STUDENTS ##################################

@app.route("/student", methods=['GET', 'POST'])
def student():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('''
            SELECT s.id, s.admission_no, s.roll_no, s.name, s.mobile, c.name AS class, sec.section 
            FROM sms_students s 
            LEFT JOIN sms_section sec ON sec.section_id = s.section 
            LEFT JOIN sms_classes c ON c.id = s.class
        ''')
        students = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()
        
        return render_template("student.html", students=students, classes=classes, sections=sections)
    
    return redirect(url_for('login'))



@app.route("/save_student", methods=['POST'])
def save_student():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'registerNo' in request.form:
            # Extract form data
            registerNo = request.form['registerNo']
            rollNo = request.form['rollNo']
            year = request.form['year']
            admission_date = request.form['admission_date']
            classid = request.form['classid']
            sectionid = request.form['sectionid']
            sname = request.form['sname']
            gender = request.form['gender']
            dob = request.form['dob']
            email = request.form['email']
            mobile = request.form['mobile']
            address = request.form['address']
            fname = request.form['fname']
            mname = request.form['mname']
            action = request.form['action']
            student_id = request.form.get('studentid')

            # Handle photo upload
            photo = None
            if 'photo' in request.files and allowed_file(request.files['photo'].filename):
                file = request.files['photo']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = filename
            
            if action == 'updateStudent':
                if photo:
                    cursor.execute('''
                        UPDATE sms_students 
                        SET admission_no = %s, roll_no = %s, class = %s, 
                            section = %s, name = %s, mobile = %s, photo = %s
                        WHERE id = %s
                    ''', (registerNo, rollNo, classid, sectionid, sname, mobile, photo, student_id))
                else:
                    cursor.execute('''
                        UPDATE sms_students 
                        SET admission_no = %s, roll_no = %s, class = %s, 
                            section = %s, name = %s, mobile = %s
                        WHERE id = %s
                    ''', (registerNo, rollNo, classid, sectionid, sname, mobile, student_id))

            else:  # Adding new student
                cursor.execute('''
                    INSERT INTO sms_students (admission_no, roll_no, academic_year, admission_date, class, section, 
                    name, photo, gender, dob, email, mobile, current_address, father_name, mother_name) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (registerNo, rollNo, year, admission_date, classid, sectionid, sname, photo, gender, dob, email, mobile, address, fname, mname))
            
            mysql.connection.commit()
            flash('Student information saved successfully!', 'success')
        
        else:
            flash('Please fill out all required fields!', 'error')
        
        return redirect(url_for('student'))

    return redirect(url_for('login'))


@app.route("/edit_student", methods=['GET', 'POST'])
def edit_student():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('''
            SELECT s.id, s.admission_no, s.roll_no, s.name, s.mobile, c.name AS class, sec.section 
            FROM sms_students s 
            LEFT JOIN sms_section sec ON sec.section_id = s.section 
            LEFT JOIN sms_classes c ON c.id = s.class 
            WHERE s.id = %s
        ''', (student_id,))
        students = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_classes')
        classes = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()
        
        if request.method == 'POST':
            registerNo = request.form['registerNo']
            rollNo = request.form['rollNo']
            classid = request.form['classid']
            sectionid = request.form['sectionid']
            sname = request.form['sname']
            mobile = request.form['mobile']
            studentid = request.form['studentid']
            action = request.form['action']

            if action == 'updateStudent':
                cursor.execute('''
                    UPDATE sms_students 
                    SET admission_no = %s, roll_no = %s, class = %s, section = %s, 
                        name = %s, mobile = %s 
                    WHERE id = %s
                ''', (registerNo, rollNo, classid, sectionid, sname, mobile, studentid))
                mysql.connection.commit()
                flash('Student information updated successfully!', 'success')
                return redirect(url_for('student'))

        return render_template("edit_student.html", students=students, classes=classes, sections=sections)
    else:
        return redirect(url_for('login'))



@app.route("/delete_student", methods=['GET'])
def delete_student():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('DELETE FROM sms_students WHERE id = %s', (student_id,))
        mysql.connection.commit()
        
        flash('Student deleted successfully!', 'success')
        return redirect(url_for('student'))
    
    return redirect(url_for('login'))