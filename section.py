########################### SECTIONS ##################################

@app.route("/sections", methods =['GET', 'POST'])
def sections():
    if 'loggedin' in session:      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_section')
        sections = cursor.fetchall()          
        return render_template("sections.html", sections = sections)
    return redirect(url_for('login')) 
    
@app.route("/edit_sections", methods =['GET'])
def edit_sections():
    if 'loggedin' in session:
        section_id = request.args.get('section_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sms_section WHERE section_id = %s', (section_id,))
        sections = cursor.fetchall() 
        return render_template("edit_section.html", sections = sections)
    return redirect(url_for('login'))    
    
@app.route("/save_sections", methods =['GET', 'POST'])
def save_sections():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if request.method == 'POST' and 'section_name' in request.form:
            section_name = request.form['section_name']                         
            action = request.form['action']             
            
            if action == 'updateSection':
                section_id = request.form['sectionid'] 
                cursor.execute('UPDATE sms_section SET section = %s WHERE section_id  =%s', (section_name, (section_id, ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO sms_section (`section`) VALUES (%s)', (section_name, ))
                mysql.connection.commit()        
            return redirect(url_for('sections'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('sections'))        
    return redirect(url_for('login')) 
    
@app.route("/delete_sections", methods =['GET'])
def delete_sections():
    if 'loggedin' in session:
        section_id = request.args.get('section_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM sms_section WHERE section_id = % s', (section_id, ))
        mysql.connection.commit()   
        return redirect(url_for('sections'))
    return redirect(url_for('login')) 