from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
app.config['SQLALCHEMY_BINDS'] = {'salasevento': 'sqlite:///salasevento.db', 'espacoscafe': 'sqlite:///espacoscafe.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    sala_evento_1 = db.Column(db.Integer)
    sala_evento_2 = db.Column(db.Integer)
    espaco_cafe_1 = db.Column(db.Integer)
    espaco_cafe_2 = db.Column(db.Integer)

    def __repr__(self):
        return '<Pessoa id: %r>' % self.id

class SalaEvento(db.Model):
    __bind_key__ = 'salasevento'
    id = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String(100), nullable=False)
    lotacao = db.Column(db.Integer)
    lotacao_real = db.Column(db.Integer)

    def __repr__(self):
        return '<Sala de Evento id: %r>' % self.id

class EspacoCafe(db.Model):
    __bind_key__ = 'espacoscafe'
    id = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String(100), nullable=False)
    lotacao = db.Column(db.Integer)

    def __repr__(self):
        return '<Espaco de Cafe id: %r>' % self.id

class Locais:
    def __init__(self, pessoa):
        self.evento_1 = SalaEvento.query.get_or_404(pessoa.sala_evento_1).nome
        self.evento_2 = SalaEvento.query.get_or_404(pessoa.sala_evento_2).nome
        self.cafe_1 = EspacoCafe.query.get_or_404(pessoa.espaco_cafe_1).nome
        self.cafe_2 = EspacoCafe.query.get_or_404(pessoa.espaco_cafe_2).nome

