from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig

from maestros import maestros
from cursos import cursos
from consultas import consultas
from inscripciones import inscripciones

import forms
from models import db, Alumnos, Maestros, Curso, Inscripciones

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(maestros)
app.register_blueprint(cursos)
app.register_blueprint(consultas)
app.register_blueprint(inscripciones)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def home():
    return render_template('bienvenida.html')

@app.route('/index')
def index():
    form = forms.UserForm(request.form)
    alumnos = Alumnos.query.all()
    return render_template('index.html', form=form, alumno=alumnos)

@app.route('/Alumnos', methods=['GET','POST'])
def alumnos():
    form = forms.UserForm(request.form)
    if request.method == 'POST' and form.validate():
        alum = Alumnos(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            telefono=form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        flash('Alumno creado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('Alumnos.html', form=form)

@app.route('/detalles', methods=['GET'])
def detalles():
    alumno_id = request.args.get('id')
    alumno = Alumnos.query.get_or_404(alumno_id)
    return render_template('detalles.html', nombre=alumno.nombre, apellidos=alumno.apellidos,
                           email=alumno.email, telefono=alumno.telefono)

@app.route('/modificar', methods=['GET','POST'])
def modificar():
    form = forms.UserForm(request.form)
    if request.method == 'GET':
        alumno_id = request.args.get('id')
        alumno = Alumnos.query.get_or_404(alumno_id)
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apellidos.data = alumno.apellidos
        form.email.data = alumno.email
        form.telefono.data = alumno.telefono
        return render_template('modificar.html', form=form)

    if form.validate():
        alumno = Alumnos.query.get_or_404(form.id.data)
        alumno.nombre = form.nombre.data
        alumno.apellidos = form.apellidos.data
        alumno.email = form.email.data
        alumno.telefono = form.telefono.data
        db.session.commit()
        flash('Alumno actualizado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('modificar.html', form=form)

@app.route('/eliminar', methods=['GET','POST'])
def eliminar():
    form = forms.UserForm(request.form)
    if request.method == 'GET':
        alumno_id = request.args.get('id')
        alumno = Alumnos.query.get_or_404(alumno_id)
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apellidos.data = alumno.apellidos
        form.email.data = alumno.email
        form.telefono.data = alumno.telefono
        return render_template('eliminar.html', form=form)

    alumno = Alumnos.query.get_or_404(request.args.get('id'))
    db.session.delete(alumno)
    db.session.commit()
    flash('Alumno eliminado correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/MaestrosAdd', methods=['GET','POST'])
def crearMaestros():
    form = forms.MaestroForm(request.form)
    if request.method == 'POST' and form.validate():
        existing = Maestros.query.filter_by(matricula=form.matricula.data).first()
        if existing:
            flash('Ya existe un maestro con esta matricula', 'danger')
            return render_template('crearMaes.html', form=form)

        maestro = Maestros(
            matricula=form.matricula.data,
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        flash('Maestro creado correctamente', 'success')
        return redirect(url_for('maestros.listado_maestros'))
    return render_template('crearMaes.html', form=form)

@app.route('/detallesMaes/<int:matricula>', methods=['GET'])
def detallesMaes(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    return render_template('detallesMaes.html', nombre=maestro.nombre,
                          apellidos=maestro.apellidos,
                          especialidad=maestro.especialidad,
                          email=maestro.email)

@app.route('/modificarMaes/<int:matricula>', methods=['GET','POST'])
def modificarMaes(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = forms.MaestroForm(request.form, obj=maestro)

    if request.method == 'POST' and form.validate():
        maestro.nombre = form.nombre.data
        maestro.apellidos = form.apellidos.data
        maestro.especialidad = form.especialidad.data
        maestro.email = form.email.data
        db.session.commit()
        flash('Maestro actualizado', 'success')
        return redirect(url_for('maestros.listado_maestros'))

    return render_template('modificarMaes.html', form=form)

@app.route('/eliminarMaes/<int:matricula>', methods=['GET','POST'])
def eliminarMaes(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = forms.MaestroForm(request.form, obj=maestro)

    if request.method == 'POST':
        db.session.delete(maestro)
        db.session.commit()
        flash('Maestro eliminado', 'success')
        return redirect(url_for('maestros.listado_maestros'))

    return render_template('eliminarMaes.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
