import os
from distutils.util import execute
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)


class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    address=db.Column(db.Text)
    city=db.Column(db.Text)
    pin=db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.name}>'
    # constructor for the model
    def __init__(self, name, address, city, pin):
      self.name = name
      self.address = address
      self.city = city
      self.pin = pin

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def new_student():
    return render_template('add.html')

@app.route('/addstd',methods=['POST','GET'])
def addstd():
    # if request.method == 'POST':
    #     try:
    #      nm=request.form['name']
    #      addr=request.form['address']
    #      city=request.form['city']
    #      pin=request.form['pin']
        
    #      with sqlite3.connect("database.db") as con:
    #             cur=con.cursor()
    #             cur.execute('INSERT INTO students (name, address,city,pin) VALUES (?, ?, ?, ?)', (nm, addr,city,pin))
    #             con.commit()
    #             msg="Успешно"
    #     except:
    #         con.rollback
    #         msg="Ошибка"
    #     finally:
    #        return render_template ("register.html", msg=msg)

    #   q = db.session.query(Students).filter(Students.pin==request.form['pin'])
    #   if db.session.query(q.exists()).scalar():
    #     msg="Студент уже был добавлен"
    if request.method=='POST':
        student=Students(
        request.form['name'],
        request.form['address'],
        request.form['city'],
        request.form['pin'])
        try:
                # if the pass number is already entered in the database, then display a notification (the number must be individual)
            q = db.session.query(Students).filter(Students.pin==request.form['pin'])
            if db.session.query(q.exists()).scalar():
                flash('Студент уже был добавлен','error')
            else:
                db.session.add(student)
                db.session.commit()
                flash('Студент успешно добавлен','success')
        except:
            flash('Ошибка при добавлении студента')
        finally:
          return redirect('/add')
    


@app.route('/list')
def list():
   # con=sqlite3.connect("database.db")
   # con.row_factory=sqlite3.Row
   # cur=con.cursor()
   # cur.execute('SELECT * from students')
   # rows=cur.fetchall()

   #students=Students.query.order_by(Students.id)
   students=Students.query.all()
   return render_template("list.html", students=students)


@app.route('/delete/<int:id>')
def delete (id):
    try:
        db.session.query(Students).filter(Students.id==id).delete()
        db.session.commit()
        return redirect('/list')
    except:
        return "error"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    
    student = db.session.query(Students).get_or_404(id)

    if request.method == 'POST':
        
        student.name=request.form['name']
        student.address=request.form['address']
        student.city=request.form['city']
        student.pin=request.form['pin']
        
        
        db.session.commit()
        return redirect('/list')
    else:
        return render_template('update.html', student=student)
