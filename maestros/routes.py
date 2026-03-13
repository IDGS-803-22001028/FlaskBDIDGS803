from flask import render_template, request, redirect, url_for
from . import maestros
from models import Maestros, db
import forms

@maestros.route("/maestros", methods=['GET','POST'])
def listado_maestros():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'POST' and create_form.validate():

        nuevo = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('maestros.listado_maestros'))

    lista_maestros = Maestros.query.all()

    # use the template name relative to the templates folder
    return render_template("maestros.html",
                           form=create_form,
                           maestros=lista_maestros)
