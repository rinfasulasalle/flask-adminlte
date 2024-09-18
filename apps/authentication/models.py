from datetime import datetime
from datetime import date

import pytz
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from apps import db

PERU_TZ = pytz.timezone('America/Lima')

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

    dni = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(PERU_TZ))

    def __init__(self, dni, nombres, apellidos, fecha_nacimiento):
        self.dni = dni
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.correo = self.generar_correo()
        self.contrasena = self.generar_contrasena()

    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apellidos}>'

    def generar_correo(self):
        primera_letra_nombre = self.nombres[0].lower()
        primer_apellido = self.apellidos.split()[0].lower()
        segundo_apellido = self.apellidos.split()[1][0].lower() if len(self.apellidos.split()) > 1 else ""
        return f"{primera_letra_nombre}{primer_apellido}{segundo_apellido}@codeguard.pe"

    def generar_contrasena(self):
        return generate_password_hash(self.dni, method='pbkdf2:sha256')

    def get_id(self):
        return self.dni

class Administracion(db.Model):
    __tablename__ = 'administracion'

    dni_usuario = db.Column(db.String(20), db.ForeignKey('usuario.dni', ondelete='CASCADE'), primary_key=True)

    def __init__(self, dni_usuario):
        self.dni_usuario = dni_usuario

    def to_dict(self):
        return {
            'dni_usuario': self.dni_usuario
        }

class Docente(db.Model):
    __tablename__ = 'docente'

    dni_usuario = db.Column(db.String(20), db.ForeignKey('usuario.dni', ondelete='CASCADE'), primary_key=True)

    def __init__(self, dni_usuario):
        self.dni_usuario = dni_usuario

    def to_dict(self):
        return {
            'dni_usuario': self.dni_usuario
        }

class Estudiante(db.Model):
    __tablename__ = 'estudiante'

    dni_usuario = db.Column(db.String(20), db.ForeignKey('usuario.dni', ondelete='CASCADE'), primary_key=True)

    def __init__(self, dni_usuario):
        self.dni_usuario = dni_usuario

    def to_dict(self):
        return {
            'dni_usuario': self.dni_usuario
        }
