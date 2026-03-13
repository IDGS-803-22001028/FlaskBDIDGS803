from flask import render_template, request, redirect, url_for, flash
from . import inscripciones
from models import Alumnos, Curso, Inscripciones, db

@inscripciones.route("/inscripciones")
def listado_inscripciones():
    lista = Inscripciones.query.all()
    return render_template("inscripciones.html", inscripciones=lista)

@inscripciones.route("/inscripciones/nuevo", methods=['GET', 'POST'])
def nueva_inscripcion():
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()
    if request.method == 'POST':
        alumno_id = request.form.get('alumno')
        curso_id = request.form.get('curso')
        if not alumno_id or not curso_id:
            flash('Selecciona alumno y curso', 'danger')
            return render_template('inscripcion_form.html', alumnos=alumnos, cursos=cursos)

        existe = Inscripciones.query.filter_by(alumno_id=alumno_id, curso_id=curso_id).first()
        if existe:
            flash('El alumno ya está inscrito en ese curso', 'warning')
            return render_template('inscripcion_form.html', alumnos=alumnos, cursos=cursos)

        insc = Inscripciones(alumno_id=alumno_id, curso_id=curso_id)
        db.session.add(insc)
        db.session.commit()
        return redirect(url_for('inscripciones.listado_inscripciones'))

    return render_template('inscripcion_form.html', alumnos=alumnos, cursos=cursos)

@inscripciones.route('/inscripciones/eliminar/<int:id>', methods=['POST'])
def eliminar_inscripcion(id):
    obj = Inscripciones.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash('Inscripción eliminada', 'success')
    return redirect(url_for('inscripciones.listado_inscripciones'))
