
from flask import Flask, Response, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    lastname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def _init_(self, name, lastname):
        self.name = name
        self.lastname = lastname

@login_manager.user_loader
def load_student(student_id):
    return Student.query.get(int(student_id))

class Profesor(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     namep = db.Column(db.String(15), unique=True)
     lastnamep = db.Column(db.String(20), unique=True)
     password = db.Column(db.String(50))
     email = db.Column(db.String(50))
    
   
class Kolegij(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv_kolegija = db.Column(db.String(15), unique=True)
    ime_prof = db.Column(db.String(20), unique=True)
    prezime_prof = db.Column(db.String(20), unique=True)

#class KolegijForm(FlaskForm):

class Prisutnost (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        prisutnost= db.Column (db.Integer)
        naziv_kolegija = db.Column (db.String(20))

class LoginForm(FlaskForm):
    name = StringField('Ime', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('Prezime', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Lozinka', validators=[InputRequired(), Length(min=8, max=50)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    name = StringField('name', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       student = Student.query.filter_by(lastname=form.lastname.data).first()
       if student:
           if check_password_hash(student.password, form.password.data):
               login_user(student)
               return redirect(url_for('student_profile'))
               return '<h1> Invalid username or password</h1>'
               
        
       
   return render_template('login.html', form=form)

@app.route("/student_profile")
@login_required
def student_profile():
    return render_template('student_profile.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/registracija", methods=['GET', 'POST'])
def registracija():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Student(name=form.name.data, lastname=form.lastname.data, password=hashed_password, email=form.email.data)  
        db.session.add(new_user)
        db.session.commit()

        return '<h1> Uspjesno ste se registrirali.</h1>'
       
    return render_template('registracija.html', form=form)

    
@app.route("/profesor_profile")
def profesor_profile():
    student = Student.query.all()
    return render_template('profesor_profile.html', student=student)



if __name__ == '__main__':
    app.run(debug=True)