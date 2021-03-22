from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import validators

from sqlalchemy.orm import relationship, lazyload
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float

import os
from aplicacion import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

#--------------------------------------Modelo base de datos-----------------------------------#

class usuarios (db.Model):
	__tablename__ = "Usuarios"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable = False)
	lastname = db.Column(db.String(50), nullable = False)
	dni = db.Column(db.String(9), nullable = False)
	address = db.Column(db.String(50), nullable = False)
	movilphone = db.Column(db.String(20), nullable = False)
	phone = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(80), nullable = False)
	password = db.Column(db.String(50), nullable = False)
	reserv_user = db.relationship('reserv', backref='owner', cascade="all, delete-orphan")

class admin (db.Model):
	__tablename__ = "Admin"
	id = db.Column(db.Integer, primary_key=True)
	admname = db.Column(db.String(50), nullable = False)
	admlastname = db.Column(db.String(50), nullable = False)
	admdni = db.Column(db.String(9), nullable = False)
	admpassword = db.Column(db.String(50), nullable = False)


class servicios (db.Model):
	__tablename__ = "Servicios"
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable = False)
	especialidad = db.Column(db.String(50), nullable = False)
	policlinica = db.Column(db.String(50), nullable = False)
	fecha = db.Column(db.String(50), nullable = False)
	horario = db.Column(db.String(50), nullable = False)
	reserv_serv = db.relationship('reserv', backref='services', cascade="all, delete-orphan", lazy='select')

class reserv (db.Model):
	__tablename__ = "reservas"
	id = db.Column(db.Integer, primary_key=True)
	atencion = db.Column(db.Integer, db.ForeignKey('Servicios.id'))
	numturnos = db.Column(db.Integer, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))


#-----------------------------sesiones administrador-------------------------------------------#


def login_user_adm(admin):
	session["id"] = admin.id
	session["admname"] = admin.admname

def logout_user_adm():
	session.pop("id",None)
	session.pop("admname", None)

#-------------------------------

def is_login_adm():
	if "admname"in session:
		return True
	else:
		False
#---------------------------------sesiones usuarios--------------------------------------#

def login_user(usuarios):
	session["id"] = usuarios.id
	session["username"] = usuarios.username


def logout_user():
	session.pop("id", None)
	session.pop("username",None)


#--------------------------------
def is_login():
	if "id" in session:
		return True
	else:
		False
#--------------------------Vistas permitidas usuario/admin ------------------------------#

@app.context_processor
def login():
	if "id" in session:
		return {'is_login':True}
	else:
		return {'is_login':False}

@app.context_processor
def admins():
	if "admname" in session:
		return {'is_login_adm':True}
	else:
		return {'is_login_adm':False}

#---------------------------------------------------------------------------------------#

#------------------------RUTAS----------------------------------------------------------#

@app.route("/")
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

#-------------------------------------REGISTRO USUARIO Y ADMINISTRADOR--------------------------------------#

@app.route("/registro", methods=["GET", "POST"])
def registro():
	if request.method == "POST":
		reguserror = " * Las contraseñas no coinciden, o el documento ya existe en el sistema"
		upass1 = request.form["contraseña"]
		upass2 = request.form["confcontraseña"]
		usuario_rep = usuarios.query.filter_by(dni=request.form["cedula"]).first()
		if usuario_rep == None and upass1 == upass2:
			passw = generate_password_hash(request.form["contraseña"], method="sha256")
			new_user = usuarios(username=request.form["names"], lastname=request.form["lastnames"],
								dni=request.form["cedula"], address=request.form["direc"],
								movilphone=request.form["telm"], phone=request.form["tel"],
								email=request.form["correo"], password = passw)
			db.session.add(new_user)
			db.session.commit()

			return render_template("msjregusu.html")
		return render_template("registro.html", reguserror = reguserror)
	return render_template("registro.html")




@app.route("/registroadmin", methods=["GET", "POST"])
def registroadmin():
	if request.method == "POST":
		regaderror = " * Las contraseñas no coinciden o el documento ya existe en el sistema"
		pass1 = request.form["admcontraseña"]
		pass2 = request.form["confadmcontraseña"]
		admin_rep = admin.query.filter_by(admdni=request.form["admcedula"]).first()
		if admin_rep == None and pass1 == pass2:
			admpassw = generate_password_hash(request.form["admcontraseña"], method="sha256")
			new_admuser = admin(admname=request.form["admnames"], admlastname=request.form["admlastnames"],
							admdni=request.form["admcedula"], admpassword = admpassw)
			db.session.add(new_admuser)
			db.session.commit()


			return render_template("msjregadmin.html")
		return render_template("registroadmin.html", regaderror = regaderror)
	return render_template("registroadmin.html")


#----------------------------------------------LOGUEO USUARIO Y ADMINISTRADOR--------------------------------------#

@app.route("/iniciar_sesion", methods=["GET","POST"])
def iniciar_sesion():
	if request.method == "POST":
		user = usuarios.query.filter_by(dni=request.form["dni_init"]).first()
		msgerror = " * Los datos ingresados son incorrectos, intente nuevamente"

		if user and check_password_hash(user.password, request.form["contraseña_init"]):
			login_user(user)
			return redirect("/servicios")

		return render_template("iniciar_sesion.html", msgerror = msgerror)

	return render_template("iniciar_sesion.html")


@app.route("/loginadmin", methods=["GET","POST"])
def loginadmin():
	if request.method == "POST":
		useradmin = admin.query.filter_by(admdni=request.form["admdni"]).first()
		msgerroradm = " * Los datos ingresados son incorrectos, intente nuevamente"

		if useradmin and check_password_hash(useradmin.admpassword, request.form["admcontraseña"]):
			login_user_adm(useradmin)
			return redirect("/infousuario")

		return render_template ("loginadmin.html", msgerroradm = msgerroradm)

	return render_template("loginadmin.html")

#--------------------------------------------- LOGOUT USUARIO Y ADMINISTRADOR--------------------------------------#

@app.route("/cerrar_sesion")
def cerrar_sesion():
	logout_user()
	return redirect(url_for('iniciar_sesion'))

@app.route("/cerrar_sesion_admin")
def cerrar_sesion_admin():
	logout_user_adm()
	return redirect(url_for('loginadmin'))

#----------------------------------eliminar usuario------------------------------------#
@app.route("/eliminar",methods=["GET","POST"])
def eliminar():
	if request.method == "POST":
		msgdel = "Se ha dado de baja del sistema correctamente ✓"
		delerror = " * La contraseña es incorrecta"

		sesionuser = session["id"]
		deleteuser = usuarios.query.filter_by(id = sesionuser).first()
		if check_password_hash(deleteuser.password, request.form["pass"]):
			db.session.delete(deleteuser)
			db.session.commit()
			logout_user()
			return render_template("servicios.html", msgdel = msgdel)
		else:
			return render_template("eliminar.html", delerror = delerror)
	return render_template("eliminar.html")


#-----------ALTA DE INFORMACION PARA EL USUARIO EN BASE DE DATOS---------------#

@app.route("/altaatenciones", methods=["GET","POST"])
def altaatenciones():
	if request.method == "POST":
		altaok = "¡Atención creada con éxito! ✓"
		servis = servicios(nombre=request.form["nombre"],
						   especialidad=request.form["especialidad"],
						   policlinica=request.form["policlinica"],
						   fecha=request.form["fecha"],
						   horario=request.form["horario"])

		db.session.add(servis)
		db.session.commit()


		return render_template("altaatenciones.html", altaok = altaok)

	return render_template("altaatenciones.html")

#--------------------MUESTREO DE INFORMACION PARA EL USUARIO------------------#

@app.route("/atenciones")
def atenciones():
	info_servicios = servicios.query.all()
	return render_template("atenciones.html", listservis = info_servicios)

@app.route("/editar", methods=["GET","POST"])
def editar():
	editok = "Ha modificado sus datos correctamente ✓ "
	datausuario = session["id"]
	datauser = usuarios.query.filter_by(id = datausuario).first()

	dataname = datauser.username
	datalastname = datauser.lastname
	datadni = datauser.dni
	dataaddress = datauser.address
	datamovil = datauser.movilphone
	dataphone = datauser.phone
	dataemail = datauser.email

	if request.method == "POST":
		datauser.username = request.form["modname"]
		datauser.lastname = request.form["modlastname"]
		datauser.dni = request.form["moddni"]
		datauser.address = request.form["modadd"]
		datauser.movilphone = request.form["modmovil"]
		datauser.phone = request.form["modphone"]
		datauser.email = request.form["modemail"]

		db.session.add(datauser)
		db.session.commit()
		return render_template("editar.html", editok = editok, dataname = dataname, datalastname = datalastname,
							datadni = datadni, dataaddress = dataaddress, datamovil = datamovil,
							dataphone = dataphone, dataemail = dataemail)


	return render_template("editar.html", dataname = dataname, datalastname = datalastname,
							datadni = datadni, dataaddress = dataaddress, datamovil = datamovil,
							dataphone = dataphone, dataemail = dataemail)

#--------------------------------------SERVICIOS DISPONIBLES PARA EL USUARIO-----------------------------------------#

@app.route("/servicios", methods=["GET"])
def show_services():
	return render_template("servicios.html")

#------------------------------------------------------------------------#
@app.route("/infousuario")
def infousuario():
    return render_template("infousuario.html")

#------------------------------------------------------------------------#

@app.route("/cancelar", methods=["GET","POST"])
@app.route("/cancelar/<cancelok>")
def cancelar():
	msg = "¡Ha Cancelado su Reserva! ✓"
	my_sesion = session["id"]
	own_reserv = reserv.query.filter_by(user_id = my_sesion).all()
	own_serv = reserv.query.filter_by(user_id = my_sesion).all()

	if request.method == "POST":
		del_reserv = reserv.query.filter_by(id = request.form["radiob"]).first()
		db.session.delete(del_reserv)
		db.session.commit()

		return render_template("cancelok.html", msg = msg)
	return render_template("cancelar.html", uuser = own_reserv, data = own_serv)

@app.route("/cancelok")
def cancelok():
	return render_template("cancelok")

#----------------------------------------------------------------#



@app.route("/reservas", methods=["GET","POST"])
def reservas():
	sesion_user = session["id"]
	owner_user = usuarios.query.filter_by(id = sesion_user).first()
	owner_reserv = reserv.query.filter_by(user_id = sesion_user).all()
	servdisp = servicios.query.all()

	if request.method == "POST":
		goturn = "¡Reserva creada con éxito!"
		userturno = " Atención elegida: " + request.form["okturno"]
		msg_cupos = "Disculpe, no quedan turnos disponibles para esta atención"

		reserv_exist = servicios.query.filter_by(id = request.form["okturno"]).first()
		number_using = reserv.query.filter_by(services = reserv_exist)

		if number_using == None:
			servis_serv = servicios.query.filter_by(id = request.form["okturno"]).first()
			sendreserv = reserv(services = servis_serv, numturnos = 1, owner = owner_user)
			db.session.add(sendreserv)
			db.session.commit()
			return render_template("reservas.html", goturn = goturn, userturno = userturno, servdisp = servdisp, uuser = owner_reserv)
		else:
			turn = 0
			if turn == 0:
				for i in number_using:
					turn = i.numturnos
			else:
				turn = 0
				for i in number_using:
					turn = i.numturnos

			if	turn < 30:
				servis_serv = servicios.query.filter_by(id = request.form["okturno"]).first()
				sendreserv = reserv(services = servis_serv, numturnos = turn + 1, owner = owner_user)
				db.session.add(sendreserv)
				db.session.commit()
				return render_template("reservas.html", goturn = goturn, userturno = userturno, servdisp = servdisp, uuser = owner_reserv)
			return render_template("reservas.html", servdisp = servdisp, uuser = owner_reserv, msg_cupos = msg_cupos)
	return render_template("reservas.html", servdisp = servdisp, uuser = owner_reserv)
	
#----------------------------------------------------------------------------------------#
@app.route("/infoatenciones", methods=["GET","POST"])
def infoatenciones():
	listados = servicios.query.all()
	
	
	if request.method == "POST":
		lista_reserva = reserv.query.filter_by(atencion=request.form["listado"])
		return render_template("inforeservas.html", list = lista_reserva)
	
	return render_template("infoatenciones.html", listados = listados)

#----------------------------------------------------------------------------------------#

@app.route("/administradores")
def administradores():
    return render_template("administradores.html")

@app.route("/gestionadmin")
def gestionadmin():
    return render_template("gestionadmin.html")

#----------------------- mensaje de registro correcto usu/adm--------#
@app.route("/msjregusu")
def msjregusu():
    return render_template("msjregusu.html")

@app.route("/msjregadmin")
def msjregadmin():
    return render_template("msjregadmin.html")
#--------------------------------------------------------------------#

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
