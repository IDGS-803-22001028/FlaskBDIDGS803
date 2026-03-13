from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Alumnos(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    inscripciones = db.relationship('Inscripciones', back_populates='alumno', cascade='all, delete-orphan')
    cursos = db.relationship('Curso', secondary='inscripciones', back_populates='alumnos')


class Maestros(db.Model):
    __tablename__ = 'maestros'

    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    cursos = db.relationship('Curso', back_populates='maestro', cascade='all, delete-orphan')


class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    maestro_id = db.Column(db.Integer, db.ForeignKey('maestros.matricula'), nullable=False)

    maestro = db.relationship('Maestros', back_populates='cursos')
    inscripciones = db.relationship('Inscripciones', back_populates='curso', cascade='all, delete-orphan')
    alumnos = db.relationship('Alumnos', secondary='inscripciones', back_populates='cursos')


class Inscripciones(db.Model):
    __tablename__ = 'inscripciones'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    alumno = db.relationship('Alumnos', back_populates='inscripciones')
    curso = db.relationship('Curso', back_populates='inscripciones')

    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'curso_id', name='uq_alumno_curso'),
    )
