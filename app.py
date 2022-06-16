import os
from flask import Flask, flash, redirect, render_template, request, session
from models import db
from webforms import LoginForm, RegisterForm
from models import Users,Students
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db.init_app(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Необходимо авторизоваться"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        new_user=Users(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect('/')
        flash('Неправильный логин или пароль')
        return  render_template('login.html',form=form)
                
    return render_template('login.html',form=form)

@app.route ('/logout')
@login_required
def logout():
    logout_user()
    session['username']=None
    return redirect('/')

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
    #       q = db.session.query(Students).filter(Students.pin==request.form['pin'])
    #       if db.session.query(q.exists()).scalar():
    #            msg="Студент уже был добавлен"
    if request.method=='POST':
        student=Students(
        request.form['name'],
        request.form['address'],
        request.form['city'],
        request.form['pin'])
 
        try:
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
@login_required
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
