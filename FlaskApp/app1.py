from flask import Flask, render_template, redirect, url_for, request, session, jsonify, json
import os
import sqlite3 as sql
import hashlib

app = Flask(__name__)

template_folder = os.path.join(os.path.dirname(__file__), "templates/")
app.static_folder = 'static'
app.static_url_path = '/static'

#File size upload not over 4MB
app.config['MAX_CONTENT_LENGTH'] = 4 * 1000 * 1000 

#Upload Folder 
UPLOAD_PROFILE_FOLDER = os.path.join(os.path.dirname(__file__), "static/profile")

app.secret_key = "I-BIT"

#Database
database = os.path.join(os.path.dirname(__file__), "database/abc_company.db")

#Upload folder
UPLOAD_IMG_FOLDER = os.path.join(os.path.dirname(__file__), "static/teams")

@app.route('/', methods=["GET"])
def index():
    session['username'] = ''
    session['audit'] = False
    return render_template("sign-in.html")

@app.route('/sign-in', methods=["GET"])
def sing_in():
    return render_template("sign-in.html")

@app.route('/sign-up', methods=["GET"]) #<a href="/sign-up">Register here</a>
def sign_up():
    return render_template("sign-up.html")

@app.route('/validate-sign-in', methods=["POST"])
def validate_sign_in():
    try:
        user = request.form['user'] #request.form.get('user')
        passwd = request.form['password']
        encrypt_pass = hashlib.md5(passwd.encode()).hexdigest()

        conn = sql.connect(database)
        cur = conn.cursor()
        sql_select = """
        SELECT username, password FROM username WHERE username = ?
        """
        val = (user,) #tuple

        cur.execute(sql_select, val)
        record = cur.fetchone()
        conn.close()
        
        if encrypt_pass == record[1]:
            session['username'] = user
            session['audit'] = True
            return redirect("/main-program")
        else: 
            return render_template("error-sign-in.html")
    except:
        return render_template("error-sign-in.html")

@app.route('/sign_in_mobile', methods=["POST"])
def validate_sign_in_mobile():
    try:
        content = request.json
        user = content['email']
        passwd = content['passwd']

        encrypt_pass = hashlib.md5(passwd.encode()).hexdigest()

        conn = sql.connect(database)
        cur = conn.cursor()
        sql_select = """
        SELECT username, password FROM username WHERE username = ?
        """
        val = (user,) #tuple

        cur.execute(sql_select, val)
        record = cur.fetchone()
        conn.close()
        
        if encrypt_pass == record[1]:
            session['username'] = user
            session['audit'] = True
            return "Login Success"
        else: 
            return redirect('/error')
    except:
        return redirect('/error')

@app.route('/validate-sign-up', methods=["POST"])
def validate_sign_up():
    fname = request.form['fname'] #request.form.get('user')
    user = request.form['user']
    passwd = request.form['password']
    cfpasswd = request.form['cfpassword']
    
    encrypt_pass = hashlib.md5(passwd.encode()).hexdigest()

    if fname !="" and user !="" and passwd !="" and passwd == cfpasswd:
        #save to db
        conn = sql.connect(database) 
        cur = conn.cursor()
        sql_insert = '''
        INSERT INTO username(username,fullname,password,authorize)
        VALUES(?,?,?,?)
        '''
        val = (user,fname,encrypt_pass,1)
        cur.execute(sql_insert,val)
        conn.commit()
        conn.close()
        return render_template("sign-up-success.html")
    else:
        return render_template("error-sign-up.html")

@app.route('/register_mobile', methods=['POST'])
def validate_sign_up_mobile():
    content = request.json
    fname = content['name'] #request.form.get('user')
    user = content['email']
    passwd = content['passwd']
    
    encrypt_pass = hashlib.md5(passwd.encode()).hexdigest()

    if fname !="" and user !="" and passwd !="":
        #save to db
        conn = sql.connect(database) 
        cur = conn.cursor()
        sql_insert = '''
        INSERT INTO username(username,fullname,password,authorize)
        VALUES(?,?,?,?)
        '''
        val = (user,fname,encrypt_pass,1)
        cur.execute(sql_insert,val)
        conn.commit()
        conn.close()
        return "Success"
    else:
        return "Error"

@app.route("/main-program", methods=["GET"])
def main_program():
    if session['audit'] == True:
        return render_template("main.html")
    else:
        return redirect("/sign-in")

@app.route("/sign-out", methods=["GET"])
def sign_out():
    session.pop('username',None)
    session.pop('audit',None)
    return redirect("/")

@app.route("/user", methods=["GET"])
def user():
    if session['audit'] == True:

        conn = sql.connect(database)
        cur = conn.cursor()
        sql_select = """
        SELECT fullname,username,authorize 
        FROM username
        ORDER BY fullname
        """
        cur.execute(sql_select)
        record = cur.fetchall() #(Tongpool Heeptaisong, tongpool.h@itd.kmutnb.ac.th, 1)
        conn.close()
        
        return render_template("user.html", user=record)
    else:
        return redirect('/sign-in')

@app.route('/user-delete/<user>', methods=["GET"])
def user_delete(user):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_delete = """
    DELETE 
    FROM username
    WHERE username=?
    """
    val = (user,)
    cur.execute(sql_delete,val)
    conn.commit()
    conn.close()
    
    return redirect("/user")

@app.route('/user-edit/<user>', methods=["GET"])
def user_edit(user):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_edit = """
    SELECT username, fullname, authorize 
    FROM username
    WHERE username=?
    """
    val = (user,)
    cur.execute(sql_edit,val)
    record = cur.fetchone()
    conn.close()
    
    return render_template('user-edit.html',user=record)

@app.route('/user-edit-post', methods=["POST"])
def user_edit_post():
    fname = request.form['fname']
    user = request.form['email']
    passwd = request.form['password']
    cfpasswd = request.form['cfpassword']

    if fname !="" and user !="":
        conn = sql.connect(database)
        cur = conn.cursor()
        sql_edit = """
        UPDATE username
        SET fullname=?
        WHERE username=?
        """
        val = (fname,user)
        cur.execute(sql_edit,val)
        conn.commit()
        conn.close()
        return redirect('/user')
    else:
        return redirect('/user')

@app.route('/user-add', methods=["GET"])
def user_add():
    return render_template('user-add.html')

@app.route('/user-add-post', methods=["POST"])
def user_add_post():
    fname = request.form['fname'] #request.form.get('user')
    user = request.form['user']
    passwd = request.form['password']
    cfpasswd = request.form['cfpassword']
    
    encrypt_pass = hashlib.md5(passwd.encode()).hexdigest()

    if fname !="" and user !="" and passwd !="" and passwd == cfpasswd:
        #save to db
        conn = sql.connect(database) 
        cur = conn.cursor()
        sql_insert = '''
        INSERT INTO username(username,fullname,password,authorize)
        VALUES(?,?,?,?)
        '''
        val = (user,fname,encrypt_pass,1)
        cur.execute(sql_insert,val)
        conn.commit()
        conn.close()
        return redirect('/user')
    else:
        return redirect('/user-add')

@app.route('/teams', methods=["GET"])
def teams():
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_query = '''
    SELECT team_id, fullname, email, images, fb, line_id, mobile
    FROM teams
    order by fullname
    '''
    cur.execute(sql_query)
    record = cur.fetchall()
    conn.close()

    return render_template('teams.html', names=record)

@app.route('/teams-add', methods=["GET"])
def teams_add():
    return render_template('teams-add.html')

@app.route('/teams-add-post', methods=["POST"])
def teams_add_post():

    fname = request.form['fname']
    email = request.form['email']
    fb = request.form['fb']
    line_id = request.form['line_id']
    mobile = request.form['mobile']
    filename = request.files['image']

    if filename !="":
        filename.save(os.path.join(UPLOAD_PROFILE_FOLDER, filename.filename))

    if fname !="" and email !="":
        conn = sql.connect(database)
        cur = conn.cursor()
        sql_insert = '''
        INSERT INTO teams(fullname,email,images,fb,line_id,mobile)
        VALUES (?,?,?,?,?,?)
        '''
        val = (fname,email,filename.filename,fb,line_id,mobile)
        cur.execute(sql_insert, val)
        conn.commit()
        conn.close()
        return redirect('/teams')
    else:
        return redirect('/teams-add')

@app.route('/teams-delete/<team_id>', methods=["GET"])
def teams_delete(team_id):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_delete = '''
    DELETE FROM teams 
    WHERE team_id=?
    '''
    val = (team_id,)
    cur.execute(sql_delete, val)
    conn.commit()
    conn.close()
    return redirect('/teams')

@app.route('/teams-edit/<team_id>', methods=["GET"])
def teams_edit(team_id):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_query = '''
    SELECT team_id, fullname, email, images, fb ,line_id, mobile
    FROM teams
    WHERE team_id=?
    '''
    val = (team_id,)
    cur.execute(sql_query, val)
    record = cur.fetchone()
    conn.close()
    return render_template('teams-edit.html', name=record)

@app.route('/teams-edit-post/<team_id>', methods=["POST"])
def teams_edit_post(team_id):
    fname = request.form['fname']
    email = request.form['email']
    fb = request.form['fb']
    line_id = request.form['line_id']
    mobile = request.form['mobile']

    filename = request.files['image']
        
    if fname !="" and email !="":
        conn = sql.connect(database)
        cur = conn.cursor()
        if filename.filename !="":
            filename.save(os.path.join(UPLOAD_PROFILE_FOLDER, filename.filename))
            sql_update = '''
            UPDATE teams 
            SET fullname=?, email=?, fb=?, line_id=?, mobile=?, images=?
            WHERE team_id=?
            '''
            val = (fname,email,fb,line_id,mobile,filename.filename,team_id)
        else:
            sql_update = '''
            UPDATE teams 
            SET fullname=?, email=?, fb=?, line_id=?, mobile=?
            WHERE team_id=?
            '''
            val = (fname,email,fb,line_id,mobile,team_id)

        cur.execute(sql_update, val)
        conn.commit()
        conn.close()
        return redirect('/teams')

    else:
        return redirect('/teams-edit' + team_id)

@app.route('/get_data_mobile', methods=["GET"])
def get_data_mobile():
    data = {
        "name": "Burin Hongprapat",
        "email": "s6307012660143@email.kmutnb.ac.th",
        "age": "21"
        }
    return jsonify(data)

# @app.route('/models/Product.dart')
# def product1():
#     with conn:
#         cur= conn.cursor()
#         cur.execute ("SELECT * FROM product")
#         rows=cur.fetchAll()
#         return render_template('Product.html',datas=rows)

@app.route('/product', methods=["GET"])
def product():
    conn = sql.connect(database)
    cursor = conn.cursor()
    sql_query = """
        SELECT product_id,title,detail,price,image,rating
        FROM product
        """
    cursor.execute(sql_query)
    product1=cursor.fetchall()
    result = []
    for row in product1:
        result.append({
            'id' : row[0],
            'title': row[1],
            'detail': row[2],
            'price' : row[3],
            'image' : row[4],
            'rating' : row[5]
    })
    conn.close()

    return {'data' : result}

    



    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)