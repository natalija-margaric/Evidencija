
from flask import Flask, Response, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
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

class Profesor(UserMixin,db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(15), unique=True)
     lastname = db.Column(db.String(20), unique=True)
     password = db.Column(db.String(50))
     email = db.Column(db.String(50))

     def _init_(self, name, lastname):
         self.name = name
         self.lastname = lastname
    
@login_manager.user_loader
def load_profesor(profesor_id):
    return Student.query.get(int(profesor_id))
   
class Kolegij(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv_kolegija = db.Column(db.String(100), unique=True)

    def _init_(self, naziv_kolegija):
        self.naziv_kolegija = naziv_kolegija
    

class KolegijForm(FlaskForm):
    naziv_kolegija = StringField ('Naziv Kolegija', validators=[InputRequired()])

class Prisutnost (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        prisutnost= db.Column (db.String)
        prezime_studenta = db.Column (db.String)
        naziv_kolegija = db.Column (db.String)
        datum = db.Column (db.String)

        def _init_(self, prisutnost, prezime_studenta, naziv_kolegija, datum):
            self.prisutnost = prisutnost
            self.prezime_studenta = prezime_studenta
            self.naziv_kolegija = naziv_kolegija
            self.datum = datum

class PrisutnostForm(FlaskForm):
       prisutnost = StringField ('')
       prezime_studenta= StringField ('') 
       naziv_kolegija =  StringField ('') 
       datum =  StringField ('') 
        

class LoginForm(FlaskForm):
    name = StringField('Ime', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('Prezime', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Lozinka', validators=[InputRequired(), Length(min=8, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class LoginProfesorForm(FlaskForm):
    name = StringField('Ime', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('Prezime', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Lozinka', validators=[InputRequired(), Length(min=8, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    name = StringField('Ime', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('Prezime', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Lozinka', validators=[InputRequired(), Length(min=8, max=80)])
    
class RegisterProfesorForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    name = StringField('Ime', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('Prezime', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Lozinka', validators=[InputRequired(), Length(min=8, max=80)])

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
               
               
        
       
   return render_template('login.html', form=form)

				
@app.route("/student_profile", methods=['GET', 'POST'])
@login_required
def student_profile():
    kolegij = Kolegij.query.all()
    profesor = Profesor.query.all()
      
    #form = PrisutnostForm()
    if request.method == "POST": 
        ime = request.form.get("ime")
        prisutnost = request.form.get("prisutnost")
        kolegij = request.form.get("kolegij")
        datum = request.form.get("datum")

	    

        new_prisutnost = Prisutnost(prisutnost=prisutnost, prezime_studenta=ime, naziv_kolegija=kolegij, datum=datum)  
        db.session.add(new_prisutnost)
        db.session.commit()
        
       
    return render_template('student_profile.html', name=current_user.name,  kolegij=kolegij, profesor=profesor,)

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

        flash('Uspjesno ste se registrirali')
        
       
    return render_template('registracija.html', form=form)

    
@app.route("/profesor_profile", methods=['GET', 'POST'])
@login_required
def profesor_profile():
    form = KolegijForm()
    if form.validate_on_submit():
        new_kolegij = Kolegij(naziv_kolegija=form.naziv_kolegija.data)
        db.session.add(new_kolegij)
        db.session.commit()

    student = Student.query.all()
    prisutnost = Prisutnost.query.all()
  
   
    return render_template('profesor_profile.html', student=student, form=form, prisutnost=prisutnost)

@app.route("/prof_log", methods=['GET', 'POST'])
def prof_log():
    form = LoginProfesorForm()
    if form.validate_on_submit():
   
       profesor = Profesor.query.filter_by(lastname=form.lastname.data).first()
       if profesor:
           if check_password_hash(profesor.password, form.password.data):
               login_user(profesor)
               return redirect(url_for('profesor_profile'))
               
    
    return render_template('prof_log.html', form=form)

@app.route("/prof_reg", methods=['GET', 'POST'])
def prof_reg():
    form = RegisterProfesorForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Profesor(name=form.name.data, lastname=form.lastname.data, password=hashed_password, email=form.email.data)  
        db.session.add(new_user)
        db.session.commit()

        return '<h1> Uspjesno ste se registrirali.</h1>'
    
    return render_template('prof_reg.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
