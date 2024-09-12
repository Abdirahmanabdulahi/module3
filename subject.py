########################### SUBJECT ##################################
    
@app.route("/subject", methods =['GET', 'POST'])
def subject():
    if 'loggedin' in session:       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_subjects')
        subjects = cursor.fetchall()          
        return render_template("subject.html", subjects = subjects)
    return redirect(url_for('login'))
    
@app.route("/save_subject", methods =['GET', 'POST'])
def save_subject():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if request.method == 'POST' and 'subject' in request.form and 's_type' in request.form and 'code' in request.form:
            subject = request.form['subject'] 
            s_type = request.form['s_type'] 
            code = request.form['code']               
            action = request.form['action']             
            
            if action == 'updateSubject':
                subjectid = request.form['subjectid'] 
                cursor.execute('UPDATE sms_subjects SET subject = %s, type = %s, code = %s WHERE subject_id  =% s', (subject, s_type, code, (subjectid, ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO sms_subjects (`subject`, `type`, `code`) VALUES (%s, %s, %s)', (subject, s_type, code, ))
                mysql.connection.commit() 
                flash("Subject Added has been saved Successfull !")       
            return redirect(url_for('subject'))        
        elif request.method == 'POST':
            flash("Please fill out the form field!")        
        return redirect(url_for('subject'))        
    return redirect(url_for('login')) 

@app.route("/edit_subject", methods =['GET'])
def edit_subject():
    if 'loggedin' in session:
        subject_id = request.args.get('subject_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT subject_id, subject, type, code FROM sms_subjects WHERE subject_id = %s', (subject_id,))
        subjects = cursor.fetchall() 
        return render_template("edit_subject.html", subjects = subjects)
    return redirect(url_for('login'))    
    
@app.route("/delete_subject", methods =['GET'])
def delete_subject():
    if 'loggedin' in session:
        subject_id = request.args.get('subject_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_subjects WHERE subject_id = % s', (subject_id, ))
        mysql.connection.commit()
        flash("Subject Delete has been Successfully !")   
        return redirect(url_for('subject'))
    return redirect(url_for('login'))
