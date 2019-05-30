
from flask import Flask, Response, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Student (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
         return f"Student('{self.username}', '{self.email}', '{self.image_file}')"

class Profesor (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False) 

    profesori= db.relationship('kolegij', backref='profesor', lazy='dynamic')
    profili=db.relationship('profil', backref='profesor', uselist=False)  

    def __repr__(self):
         return f"Profesor('{self.username}', '{self.email}', '{self.image_file}')" 


    class Kolegij (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        Naziv = db.Column(db.String(20))

        profesor_id= db.Column(db.Integer, db.ForeignKey('profesor.id'))
        prisutnosti=db.relationship('prisutnost', backref='kolegij', lazy='dynamic')

        def __repr__(self):
         return f"kolegij('{self.naziv})" 

    db.Table('profil_kolegij',)
    db.Column('profil_id', db.Integer, db.ForeignKey('profil.id')),
    db.Column('kolegij_id', db.Integer, db.ForeignKey('kolegij.id'))
   
        

    class Profil (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        Ime: db.Column(db.String(30))
        Prezime: db.Column(db.String(30))
        Profesor_id = db.Column(db.Integer)
        Student_jmbag = db.Column(db.Integer)

        prof_id = db.Column(db.Integer, db.ForeignKey('profesor.id'), unique=True)
stud_id= db.Column(db.Integer, db.ForeignKey ('student.id'), unique=True)
kolegiji=db.relationship ('kolegij', secondary='profil_kolegij', backref='profil', lazy='dynamic')

def __repr__(self):
         return f"profil('{self.ime}', '{self.prezime}')"

    class Prisutnost (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        Ucenici_jmbag = db.Column (db.Integer)
        Naziv_kolegija = db.Column (db.String(20))


@app.route("/")
@app.route("/home")
def home():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)