from wtforms import Form,StringField, IntegerField, EmailField, validators


class UserForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.Length(min=4, max=20, message='requiere min=4 max=20')
    ])
    apellidos = StringField('apellidos', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    email = EmailField('correo', [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El teléfono es requerido'),
        validators.Regexp(r'^\d{10}$', message='El teléfono debe contener exactamente 10 dígitos')
    ])
  