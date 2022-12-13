import os
from flask import Flask, render_template, flash, request, redirect, session, url_for
from flask_session import Session
from datetime import datetime, timedelta
from forms import LoginForm, ChangeNumberForm, TransferForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#Create a flask instance
app = Flask(__name__, template_folder='templates')

#Set up session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
Session(app)

#Create a secret key for CSRF protection
app.config['SECRET_KEY'] = 'SECRET_KEY'

#Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:beckwith278@localhost:3306/Banking_Database'

#Initialize the database
db = SQLAlchemy(app)

#Create a login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user_info.query.get(int(user_id))


class user_info(db.Model, UserMixin):
    customer_id = db.Column(db.Integer, primary_key = True)
    account_number = db.Column(db.Integer(), unique = True)
    username = db.Column(db.String(20), unique = True)
    passwd = db.Column(db.String(18))

    def get_id(self):
           return (self.customer_id)
    def is_authenticated(self):
          return super().is_authenticated
    def is_active(self):
          return super().is_active

class customer_info(db.Model):
    customer_name = db.Column(db.String(32))
    credit_score = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(45))
    state = db.Column(db.String(25))
    account_number = db.Column(db.Integer)
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(10))

class bank_department(db.Model):
      location = db.Column(db.String(50))
      name = db.Column(db.String(25))
      department_id = db.Column(db.Integer, primary_key = True)

class bank_branches(db.Model):
      branch_name =  db.Column(db.String(32))
      branch_id = db.Column(db.Integer, primary_key = True)
      branch_city = db.Column(db.String(32))
      department_id = db.Column(db.Integer)

class accounts(db.Model):
      account_number =  db.Column(db.Integer, primary_key = True)
      customer_id = db.Column(db.Integer)
      account_type = db.Column(db.String(32))
      balance = db.Column(db.Float)
      routing_number = db.Column(db.String(16))
      department_id = db.Column(db.Integer)

class loans(db.Model):
      loan_type =  db.Column(db.String(15))
      loan_id = db.Column(db.Integer, primary_key = True)
      interest = db.Column(db.Float)
      amount = db.Column(db.Integer)
      duration = db.Column(db.Integer)

# Create a route decorator
@app.route('/')

def index():
    form = LoginForm()
    if not session.get("name"):
        return render_template("login.html", form = form)
    return render_template("dashboard.html")

# localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    if not session.get("username"):
        flash("Please login first!")
        return redirect(url_for('login'))
    return render_template("user.html", user_name=name)

#Invalid URL
@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)

def page_not_found(e):
    return render_template("500.html"), 500

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if form is submitted
    if form.validate_on_submit():
        #get the username and password
        username = request.form.get('username')
        password = request.form.get('password')
        #Check if the username and password are correct
        user = user_info.query.filter_by(username = username).first()
        if user:
            if user.passwd == password:
                flash("Logged in successfully!")
                login_user(user, remember=True)
                session["username"] = username
                session["id"] = user.customer_id
                return redirect(url_for('dashboard'))
    return render_template("login.html", form = form)

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    form = TransferForm()
    if not session.get("username"):
        flash("Please login first!")
        return redirect(url_for('login'))
    
    savings = accounts.query.filter_by(account_type = "Savings", customer_id = session["id"]).all()
    checking = accounts.query.filter_by(account_type = "Checking", customer_id = session["id"] ).all()
    all_accounts = accounts.query.filter_by(customer_id = session["id"]).all()
    return render_template("dashboard.html", savings = savings, checking = checking, all_accounts = all_accounts, form=form)


# Logout Page
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('index'))

# Create change number page
@app.route('/changeNumber', methods=['GET', 'POST'])
def change_number():
    #change_number = None
    form = ChangeNumberForm()
    #number_to_update = user_info.query.get_or_404(id)
    if form.validate_on_submit():
        flash("Phone number changed successfully!")
    return render_template("changeNumber.html", form=form)

#Transfer
@app.route('/transfer', methods=['POST'])
def transfer():
    form = TransferForm()
    if not session.get("username"):
        flash("Please login first!")
        return redirect(url_for('login'))
    if form.validate_on_submit():
        #get the username and password
        to_account = request.form.get('to_account')
        from_account = request.form.get('from_account')
        amount = request.form.get('amount')
        #Can't transfer to the same account
        if to_account == from_account:
            flash("You cannot transfer to the same account!")
            return redirect(url_for('dashboard'))
        #Check if the accounts exist
        if not accounts.query.filter_by(account_number = from_account, customer_id = session["id"]).first():
            flash("From Account does not exist!")
            return redirect(url_for('dashboard'))
        #Check if the accounts exist
        if not accounts.query.filter_by(account_number = to_account, customer_id = session["id"]).first():
            flash("To Account does not exist!")
            return redirect(url_for('dashboard'))
        from_account_balance = accounts.query.filter_by(account_number = from_account, customer_id = session["id"]).first().balance
        #Check if the account has enough funds
        if from_account_balance < float(amount):
            flash("Insufficient funds!")
            return redirect(url_for('dashboard'))
        if float(amount) <= 0:
            flash("Amount must be greater than 0!")
            return redirect(url_for('dashboard'))
        #Update the balance of the from account
        from_account_balance = from_account_balance - float(amount)
        accounts.query.filter_by(account_number = from_account, customer_id = session["id"]).first().balance = from_account_balance
        #Update the balance of the to account
        to_account_balance = accounts.query.filter_by(account_number = to_account, customer_id = session["id"]).first().balance
        to_account_balance = to_account_balance + float(amount)
        accounts.query.filter_by(account_number = to_account, customer_id = session["id"]).first().balance = to_account_balance
        db.session.commit()
        flash("Transfer successful!")
        return redirect(url_for('dashboard'))
    else:
        flash("Transfer failed!")
    return redirect(url_for('dashboard'))
        
    

if __name__ == '__main__':
    app.run(debug=True)