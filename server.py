from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = "ThisisSecretone"
mysql = MySQLConnector(app,'mydb')
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/users')
def showTemplate():
	user_query = "SELECT * FROM usersRestful"
	user = mysql.query_db(user_query)
	return render_template("display.html", all_users = user)

@app.route('/users/new')
def addUserDisplay():
	return render_template("/newusers.html")

@app.route('/users/create', methods=['POST'])
def create_user():
	user_query = "SELECT * FROM usersRestful WHERE email = :email LIMIT 1"
	query_data = { 'email': request.form['email'] }
	user = mysql.query_db(user_query, query_data)
	counter = 0

	if user:
		flash("Email Already In Use!!", "error")
		counter += 1
	if len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1 or len(request.form['email']) < 1:
		flash("Field Inputs must not be empty", 'error')
		counter += 1
	if len(request.form['first_name']) < 2 or len(request.form['last_name']) < 2:
		flash("First and Last name must be at least 2 characters")
		counter += 1
	if request.form['first_name'].isalpha() == False or request.form['last_name'].isalpha() == False:
		flash("First and Last name must contain only alphabetic characters", 'error')
		counter += 1
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address", 'green')
		counter += 1
	if counter == 0:
		query = "INSERT INTO usersRestful (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
		data = {
	             'first_name': request.form['first_name'], 
	             'last_name':  request.form['last_name'],
	             'email': request.form['email'],
	           }
		mysql.query_db(query, data)
		return redirect('/users')
	else:
		return redirect('/users/new')

@app.route('/users/<id>')
def showOneUser(id):
	user_query = "SELECT * FROM usersRestful where id = :id"
	query_data = {'id': id}
	user = mysql.query_db(user_query, query_data)
	return render_template("users.html", one_user = user)

@app.route('/users/<id>/edit')
def updateUserDisplay(id):
	user_query = "SELECT * FROM usersRestful where id = :id"
	query_data = {'id': id}
	user = mysql.query_db(user_query, query_data)
	return render_template("edit.html", edit_user = user)

@app.route('/users/<id>', methods = ['POST'])
def updateUser(id):
	counter = 0
	if len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1 or len(request.form['email']) < 1:
		flash("Field Inputs must not be empty", 'error')
		counter += 1
	if len(request.form['first_name']) < 2 or len(request.form['last_name']) < 2:
		flash("First and Last name must be at least 2 characters")
		counter += 1
	if request.form['first_name'].isalpha() == False or request.form['last_name'].isalpha() == False:
		flash("First and Last name must contain only alphabetic characters", 'error')
		counter += 1
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address", 'green')
		counter += 1
		
	if counter == 0:
		query = "UPDATE usersRestful SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
		data = {
		     'first_name': request.form['first_name'], 
		     'last_name':  request.form['last_name'],
		     'email': request.form['email'],
		     'id': id
		   }
		mysql.query_db(query, data)
		return redirect('/users')
	else:
		return redirect('/users')

@app.route('/users/<id>/delete')
def deleteUser(id):
    query = "DELETE FROM usersRestful WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/users')

app.run(debug=True) # run our server
