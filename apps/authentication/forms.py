# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    dni = StringField('DNI',
                        id='dni_login',
                        validators=[DataRequired(), Length(min=8, max=20)])
    contrasena = PasswordField('Contraseña',
                                id='pwd_login',
                                validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    dni = StringField('DNI',
                        id='dni_create',
                        validators=[DataRequired(), Length(min=8, max=20)])
    nombres = StringField('Nombres',
                            id='nombres_create',
                            validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos',
                            id='apellidos_create',
                            validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento',
                                    id='fecha_nacimiento_create',
                                    format='%Y-%m-%d',
                                    validators=[DataRequired()])
