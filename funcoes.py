from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from classes import Pessoa, SalaEvento, EspacoCafe, Locais

def atualiza_lotacao_real(db, salas):
    lotacao_minima = db.session.query(func.min(SalaEvento.lotacao)).scalar()
    for sala in salas:
        if sala.lotacao > lotacao_minima:
            sala.lotacao_real = lotacao_minima + 1
        else:
            sala.lotacao_real = lotacao_minima
    try:
        db.session.commit()
    except:
        return 'Houve um problema ao atualizar os dados de lotacao das salas'

def calcula_lotacao_maxima(salas, cafes):
    lotacao_salas = 0
    for sala in salas:
        lotacao_salas += sala.lotacao_real
    
    lotacao_cafes = 0
    for cafe in cafes:
        lotacao_cafes += cafe.lotacao
    
    if lotacao_cafes < lotacao_salas:
        return lotacao_cafes
    else:
        return lotacao_salas
