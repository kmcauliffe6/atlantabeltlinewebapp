import pymysql
from flask import Flask, request, render_template, redirect, url_for, flash, session

app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             passwd='13',
                             db='phase3data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@app.route("/")
def setup():
    return render_template('home.html')

#registration methods
@app.route('/registernavigation')
def registernavigation():
    return render_template('register_navigation.html')

@app.route('/back')
def back_to_home():
    return render_template('home.html')

@app.route('/register_user')
def register_user():
    return render_template('register.html')

@app.route('/register_visitor')
def register_visitor():
    return render_template('register_visitor.html')

@app.route('/register_employee')
def register_employee():
    return render_template('register_employee.html')

@app.route('/register_employee_visitor')
def register_employee_visitor():
    return render_template('register_employee_visitor.html')

#NOTE: should probably add hashing for passwords
@app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            emails = request.form['email'].split(',')
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                for eemail in emails:
                    sql2 = "INSERT INTO User_Email(UEmail, UUsername) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                    cursor.execute(sql2)
                connection.commit()
                session['username'] = request.form['username']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("One of your emails is already being used. Please try again", 'alert-error')
    return render_template('register.html')


@app.route('/register_visitor_buttonclick', methods=['GET','POST'])
def register_visitor_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                    sql2 = "INSERT INTO User_Email(UEmail, UUsername) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                    cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("One of your emails is already being used. Please try again", 'alert-error')
            sql3 = "INSERT INTO Visitor(VisUsername) VALUES ('{username}')".format(username = request.form['username'])
            try:
                cursor.execute(sql3)
                connection.commit()
                session['email'] = request.form['email']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong.", 'alert-error')
        return render_template('register_visitor.html')

#these two are giving integrity errors for everything??
@app.route('/register_employee_buttonclick', methods=['GET','POST'])
def register_employee_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                        sql2 = "INSERT INTO User_Email(UEmail, UUsername) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                        cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("That email already exists. Please try again.", 'alert-error')
            sql3 = "INSERT INTO Employee(EUsername, Phone, EmployeeID, Address, City, State, Zipcode) VALUES ('{username}', '{phone}', '{id}', '{address}', '{city}', '{state}', '{zipcode}');".format(username = request.form['username'], phone = request.form['phone'], id = 111, address = request.form['address'], city = request.form['city'], state = request.form['state'], zipcode = request.form['zipcode'])
            if request.form['User Type'] == "Manager":
                sql4 = "INSERT INTO Manager(MngUsername) VALUES ('{username}')".format(username = request.form['username'])
            else:
                sql4 = "INSERT INTO Staff(StaffUsername) VALUES ('{username}')".format(username = request.form['username'])
            #need to get employee ID??
            try:
                cursor.execute(sql3)
                cursor.execute(sql4)
                connection.commit()
                session['email'] = request.form['email']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong", 'alert-error')
    return render_template('register.html')
@app.route('/register_employee_visitor_buttonclick', methods=['GET','POST'])
def register_employee_visitor_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                        sql2 = "INSERT INTO User_Email(UEmail, UUsername) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                        cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("That email already exists. Please try again.", 'alert-error')
            sql3 = "INSERT INTO Employee(EUsername, Phone, EmployeeID, Address, City, State, Zipcode) VALUES ('{username}', '{phone}', '{id}', '{address}', '{city}', '{state}', '{zipcode}');".format(username = request.form['username'], phone = request.form['phone'], id = 111, address = request.form['address'], city = request.form['city'], state = request.form['state'], zipcode = request.form['zipcode'])
            if request.form['User Type'] == "Manager":
                sql4 = "INSERT INTO Manager(MngUsername) VALUES ('{username}')".format(username = request.form['username'])
            else:
                sql4 = "INSERT INTO Staff(StaffUsername) VALUES ('{username}')".format(username = request.form['username'])
            sql5 = "INSERT INTO Visitor(VisUsername) VALUES ('{username}')".format(username = request.form['username'])
            #need to get employee ID
            try:
                cursor.execute(sql3)
                cursor.execute(sql4)
                cursor.execute(sql5)
                connection.commit()
                session['email'] = request.form['email']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong. Please try again.", 'alert-error')
    return render_template('register_employee_visitor.html')

#login methods
@app.route('/login', methods=['GET','POST'])
def login():
    #currently checking username and password, need to write queries to check
    #email and password
    if (request.method == 'POST'):
        sql1 = "SELECT UUsername FROM User_Email WHERE UEmail = '{email}'".format(email = request.form['email'])
        result = cursor.execute(sql1);
        username = ""
        for row in cursor:
            username = row['UUsername']
        sql2 = "SELECT * FROM  User WHERE Username = '{username1}' AND Password = '{password}'".format(username1 = username, password = request.form['password'])
        result = cursor.execute(sql2);
        if result: #if any rows returned aka username was found
            row = cursor.fetchone()
            session['email'] = row.get('email') #keep track of current user
            getUserType(username)
            correctpage = goToCorrectFunctionalityPage()
            print(username)
            print(session['user_type'])
            return render_template('{page}'.format(page = correctpage))
        else:
            flash("Incorrect Credentials. Please Try Again.", 'alert-error')
    return render_template('home.html')

#user function methods
@app.route('/take_transit')
def take_transit():
    return render_template('user_take_transit.html')
@app.route('/view_transit_history')
def view_transit_history():
    return render_template('user_view_transit_history.html')

@app.route('/go_to_user_functionality')
def go_to_user_functionality():
    return render_template("user_functionality.html")
#helper methods
def getUserType(username):
    print(username)
    #need to add visitor/user case
    sql = "SELECT * FROM Manager WHERE MngUsername = '{username1}'".format(username1 = username)
    sql2 = "SELECT * FROM Visitor WHERE VisUsername = '{username1}'".format(username1 = username)
    result = cursor.execute(sql)
    result2 = cursor.execute(sql2)
    if result and result2:
        session['user_type'] = "manager-visitor"
        return;
    sql = "SELECT * FROM Manager WHERE MngUsername = '{username1}'".format(username1 = username)
    result = cursor.execute(sql)
    if result:
        session['user_type'] = "manager"
        return;
    sql = "SELECT * FROM Staff WHERE StaffUsername = '{username1}'".format(username1 = username)
    result = cursor.execute(sql)
    if result:
        session['user_type'] = "staff"
        return;
    sql = "SELECT * FROM Visitor WHERE VisUsername = '{username1}'".format(username1 = username)
    result = cursor.execute(sql)
    if result:
        session['user_type'] = "visitor"
        return;
    sql = "SELECT * FROM User WHERE Username = '{username1}'".format(username1 = username)
    result = cursor.execute(sql)
    if result:
        session['user_type'] = "user"
        return;

def goToCorrectFunctionalityPage():
    if session['user_type'] == 'user':
       return 'user_functionality.html'
    if session['user_type'] == "visitor":
        return 'visitor_functionality.html'
    if session['user_type'] == "manager":
        return 'manager_functionality.html'
    if session['user_type'] == "manager-visitor":
        return "manager_visitor_functionality.html"

if __name__ == "__main__":
    app.secret_key = 'supersecretkey'
    app.run(debug=True)



