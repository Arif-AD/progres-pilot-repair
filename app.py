from flask import Flask, render_template, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates/')
app.secret_key = '!@#$%'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_pilot_repair'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'tb_akses'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nomor_hp = db.Column(db.String(15))
    password = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    email_error = None
    passwd_error = None

    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        user = User.query.filter_by(email=email).first()

        if not email:
            email_error = 'Email Tidak Boleh Kosong'
        elif not user:
            email_error = 'Email tidak terdaftar. Silakan daftar terlebih dahulu.'

        if not passwd:
            passwd_error = 'Password Tidak Boleh Kosong'
        elif user and passwd != user.password:  # Periksa apakah password sesuai
            passwd_error = 'Password Yang Anda Masukan Salah'

        if user and not email_error and not passwd_error:  # Jika email dan password sesuai, masuk
            session['is_logged_in'] = True
            session['username'] = user.nama
            session['email'] = user.email 
            session['nomor_hp'] = user.nomor_hp
            return redirect(url_for('index'))
        else:
            return render_template('login.html', email_error=email_error, passwd_error=passwd_error)
    else:
        return render_template('login.html', email_error=email_error, passwd_error=passwd_error)


@app.route("/logout")
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    
    pesan_error = None
    email_error = None
    
    if request.method == 'POST' and 'inpNama' in request.form and 'inpEmail' in request.form and 'inpNomor' in request.form and 'inpPass' in request.form:
        username = request.form['inpNama']
        email = request.form['inpEmail']
        nomor_hp = request.form['inpNomor']
        passwd = request.form['inpPass']
        user_tersedia = User.query.filter_by(email=email).first()
    
        if not username or not email or not nomor_hp or not passwd:
            pesan_error = 'Wajib Diisi'
            
        if user_tersedia:
            email_error = 'Email Sudah terdaftar. Silahkan gunakan email lain'
        
        else:
            user = User(nama=username, email=email, nomor_hp=nomor_hp, password=passwd)
            db.session.add(user)
            db.session.commit()
            
            session['is_logged_in'] = True
            session['username'] = email
            
            return redirect(url_for('login'))
        
    else:
        return render_template('register.html', email_error=email_error, pesan_error=pesan_error)


@app.route("/profile")
def profile():
     return render_template('profile.html', title='profile')


@app.route("/about")
def about():
    return render_template('about.html')

# @app.route("/home")
# def home():
#     users = User.query.all()
#     return render_template('home.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
