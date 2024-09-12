################################ Classes  #######################################

@app.route("/classes", methods =['GET', 'POST'])
def classes():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT c.id, c.name, s.section, t.teacher FROM sms_classes c LEFT JOIN sms_section s ON s.section_id = c.section LEFT JOIN sms_teacher t ON t.teacher_id = c.teacher_id')
        classes = cursor.fetchall() 
           
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM sms_teacher')
        teachers = cursor.fetchall()
        
        return render_template("class.html", classes = classes, sections = sections, teachers = teachers)
    return redirect(url_for('login'))

@app.route("/edit_class", methods =['GET'])
def edit_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT c.id, c.name, s.section, t.teacher FROM sms_classes c LEFT JOIN sms_section s ON s.section_id = c.section LEFT JOIN sms_teacher t ON t.teacher_id = c.teacher_id WHERE c.id = %s', (class_id,))
        classes = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM sms_teacher')
        teachers = cursor.fetchall()
        
        return render_template("edit_class.html", classes = classes, sections = sections, teachers = teachers)
    return redirect(url_for('login'))  

@app.route("/save_class", methods =['GET', 'POST'])
def save_class():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if request.method == 'POST' and 'cname' in request.form:
            cname = request.form['cname'] 
            sectionid = request.form['sectionid']
            teacherid = request.form['teacherid']            
            action = request.form['action']             
            
            if action == 'updateClass':
                class_id = request.form['classid'] 
                cursor.execute('UPDATE sms_classes SET name = %s, section = %s, teacher_id = %s WHERE id  =%s', (cname, sectionid, teacherid, (class_id, ), ))
                mysql.connection.commit() 
                flash("Data Updated has been Successfully!", "success")       
            else: 
                cursor.execute('INSERT INTO sms_classes (`name`, `section`, `teacher_id`) VALUES (%s, %s, %s)', (cname, sectionid, teacherid))
                mysql.connection.commit()
                flash("Data Saved has been Successfully!", "success")         
            return redirect(url_for('classes'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('classes'))        
    return redirect(url_for('login'))
    

@app.route("/delete_class", methods =['GET'])
def delete_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_classes WHERE id = % s', (class_id, ))
        mysql.connection.commit() 
        flash("Data Deleted has been Successfully!", "danger")   
        return redirect(url_for('classes'))
    return redirect(url_for('login')) 