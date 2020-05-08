#---------------------------------------------------------
#import
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from wtforms.validators import DataRequired, URL
import time
hak = 0
#----------------------------------------------------------
#kayit formu
class RegisterFrom(Form):
    name = StringField('Isim Soyisim', validators=[DataRequired(message='Lütfen isim ve soyisim yaziniz')])
    username = StringField('Kulanici Adi', validators=[validators.DataRequired(message="Lütfen kulanici adinizi yaziniz"),validators.length(min =4, max=30 ,message="Kulanici adiniz en az 4 karakter oluşmali")])
    email = StringField('Mail', validators=[validators.DataRequired(message='Lütfen mail adresinizi yaziniz'),validators.Email(message="lütfen geçerli mail adressi giriniz.")])
    password = PasswordField("Parola :",validators=[
    validators.DataRequired(message= "Lutfen geçerli parola belirleyin."),
    validators.EqualTo(fieldname = "confrim",message="Paraloniz uyuşmiyor.")])
    confrim = PasswordField("Parola Doğurla",validators=[validators.DataRequired(message="Lütfen parolayi onaylayin")])
#-------------------------------------------------------------------------------------------------------------------------------
class LoginForm(Form):
    username = StringField("Kulanici adi",validators=[validators.DataRequired("Lutfen Kulanici adiniz giriniz")])
    password = PasswordField("Parola",validators=[validators.DataRequired("Lutfen parolanizi giriniz")])

#-------------------------------------------------
#app
app = Flask(__name__)
app.secret_key = "woxyblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "woxyblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)
#--------------------------------------------------

#ansayfa
@app.route("/")
def home():
    return render_template("layout.html")
#-------------------------------------------------
#hakkimda
@app.route("/hakkımda")
def about():
    return render_template("hakkımda.html")
#-----------------------------------------------
#kayit olma
@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterFrom(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password =sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("Başariyla kayit oldunuz şimdi giris yapabilirsiniz","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)
#---------------------------------------------------------------------------------------
#bakimda
@app.route("/makale/<string:id>")
def detail(id):
    return "makale id :"+ id
#----------------------------------------------------------------------------------------
#login
@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entred = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s "
        result = cursor.execute(sorgu,(username,))
        if result > 0 :
            data = cursor.fetchone()
            realpassword = data["password"]
            if sha256_crypt.verify(password_entred,realpassword):
                flash("Başariyla giriş yaptiniz","success")
                session["logged_in"] = True
                return redirect(url_for("home"))
            else:
                flash("Parolaniz yanliş girdiniz","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kulanici bunulanmadi....","danger")
            return redirect(url_for("login"))      
    return render_template("login.html",form=form)
#--------------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))




#---------------------------------
#defult
if __name__ == "__main__":
    app.run(debug=True)
#---------------------------------

