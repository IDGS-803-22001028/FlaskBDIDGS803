from flask import render_template, request
from . import consultas
from models import Curso, Alumnos

@consultas.route("/alumnos_por_curso", methods=['GET','POST'])
def alumnos_por_curso():

    cursos = Curso.query.all()
    alumnos = None

    if request.method == 'POST':

        curso_id = request.form['curso']

        curso = Curso.query.get(curso_id)

        alumnos = curso.alumnos

    return render_template(
        "consulta_alumnos.html",
        cursos=cursos,
        alumnos=alumnos
    )


@consultas.route("/cursos_por_alumno", methods=['GET','POST'])
def cursos_por_alumno():

    alumnos_lista = Alumnos.query.all()
    cursos = None

    if request.method == 'POST':

        alumno_id = request.form['alumno']

        alumno = Alumnos.query.get(alumno_id)

        cursos = alumno.cursos

    return render_template(
        "consulta_cursos.html",
        alumnos=alumnos_lista,
        cursos=cursos
    )