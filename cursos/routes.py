from flask import render_template, request, redirect, url_for, flash
from . import cursos
from models import Curso, Maestros, db

@cursos.route("/cursos", methods=['GET'])
def listado_cursos():
    lista_cursos = Curso.query.all()
    return render_template("cursos.html", cursos=lista_cursos)

@cursos.route('/crearCurso', methods=['GET','POST'])
def crear_curso():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        maestro_id = request.form.get('maestro')

        if not nombre or not maestro_id:
            flash('El nombre y el maestro son obligatorios', 'danger')
        else:
            nuevo = Curso(nombre=nombre, descripcion=descripcion, maestro_id=maestro_id)
            db.session.add(nuevo)
            db.session.commit()
            # no mostrar alerta al crear curso según petición del usuario
            return redirect(url_for('cursos.listado_cursos'))

    lista_maestros = Maestros.query.all()
    return render_template('crearCurso.html', maestros=lista_maestros)

@cursos.route('/cursos/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_curso(id):
    curso = Curso.query.get_or_404(id)

    if request.method == 'POST':
        curso_nombre = request.form.get('nombre')
        curso_descripcion = request.form.get('descripcion')
        curso_maestro_id = request.form.get('maestro')

        if not curso_nombre or not curso_maestro_id:
            flash('Nombre y maestro son requeridos', 'danger')
        else:
            curso.nombre = curso_nombre
            curso.descripcion = curso_descripcion
            curso.maestro_id = curso_maestro_id
            db.session.commit()
            flash('Curso actualizado', 'success')
            return redirect(url_for('cursos.listado_cursos'))

    maestros = Maestros.query.all()
    return render_template('modificarCurso.html', curso=curso, maestros=maestros)

@cursos.route('/cursos/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(curso)
        db.session.commit()
        # no mostrar alerta adicional al eliminar, solo redirigir
        return redirect(url_for('cursos.listado_cursos'))

    # GET -> mostrar página de confirmación
    return render_template('eliminarCurso.html', curso=curso)