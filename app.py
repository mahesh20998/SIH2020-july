from flask import Flask, render_template, request,redirect, url_for,g,session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask import flash
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
app.config['MySQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sih'

mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/create_account', methods = ['GET', 'POST'])
def create_account():
	if request.method == 'POST':
		cursor = mysql.connection.cursor()
		uname = request.form.get('uname')
		cursor.execute("SELECT * FROM register WHERE uname = %s", [uname])
		if cursor.fetchone() is not None:
			flash("That username is already taken...", "error")
			return render_template('create-account.html')
		else:
			fname = request.form.get('fname')
			mname = request.form.get('mname')
			lname = request.form.get('lname')
			email = request.form.get('email')
			dob = request.form.get('dob')
			phone = request.form.get('phone')
			address = request.form.get('address')
			state = request.form.get('state')
			city = request.form.get('city')
			gender = request.form.get('gender')
			description = request.form.get('fname')
			password = request.form.get('password')
			password = pwd_context.hash(password)
			profpic = request.files['profpic']
		
		

		sql_insert_blob_query = """ INSERT INTO register(uname, fname, mname, lname,phone, email, dob, address, sex, city, state, password, profpic, descr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		cursor.execute(sql_insert_blob_query,(uname, fname, mname, lname,phone, email, dob, address, gender, city, state, password, profpic, description))
		mysql.connection.commit()
		cursor.close()
		
		flash('You are now registered and can log in', 'success')
		return redirect(url_for('login'))
	return render_template('create-account.html')


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        cursor = mysql.connection.cursor()
        uname = request.form.get('uname')
        password = request.form.get('password')
        result = cursor.execute("SELECT * FROM register WHERE uname = %s", [uname])
        if result > 0:
            data = cursor.fetchone()
            password_db = data[11]
            flash(password_db)
            flash(password)
            if (pwd_context.verify(password, password_db)):
                session['logged_in'] = True
                session['username'] = uname
                flash('You are now logged in', 'success')
                return redirect(url_for('pofile'))
            else:
                flash('Invalid Login', 'error')
                return render_template('login.html')
            cursor.close()
        else:
            flash('User not found', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/pofile')
def pofile():
	return render_template('tp.html')


if __name__ == '__main__':
	app.secret_key =  'mahesh'
	app.run(debug=True)