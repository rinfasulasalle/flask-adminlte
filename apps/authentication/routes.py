# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from datetime import datetime
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Usuario

from werkzeug.security import check_password_hash, generate_password_hash


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST':

        # Read form data
        dni = request.form['dni']
        contrasena = request.form['contrasena']

        # Locate user
        user = Usuario.query.filter_by(dni=dni).first()

        # Check the password
        if user and check_password_hash(user.contrasena, contrasena):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                                msg='DNI o contraseña incorrectos',
                                form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                                    form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)

    if request.method == 'POST' and create_account_form.validate_on_submit():
        dni = request.form['dni']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento_str = request.form['fecha_nacimiento']

        # Convertir la fecha de nacimiento de cadena a objeto date
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            return render_template('accounts/register.html',
                                    msg='Fecha de nacimiento no válida',
                                    success=False,
                                    form=create_account_form)

        # Check DNI exists
        user = Usuario.query.filter_by(dni=dni).first()
        if user:
            return render_template('accounts/register.html',
                                    msg='DNI ya registrado',
                                    success=False,
                                    form=create_account_form)

        # Crear el usuario
        user = Usuario(dni=dni, nombres=nombres, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                                msg='Usuario creado, ingresar a <a href="/login">login</a>',
                                success=True,
                                form=create_account_form)

    return render_template('accounts/register.html', form=create_account_form)
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
