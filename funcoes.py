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

def troca_de_sala(sala_atual, ultima_sala, numeracao):
    if numeracao % 2 == 0:
        if sala_atual == ultima_sala:
            return 1
        else:
            return sala_atual + 1
    else:
        return sala_atual

def sala_nao_lotada(sala_atual, lotacao_minima):
    id_sala = sala_atual
    achou_sala = False
    while not achou_sala:
        sala = SalaEvento.query.get_or_404(id_sala)
        if sala.lotacao_real > lotacao_minima:
            achou_sala = True
        else:
            id_sala += 1 
    return id_sala

def atualiza_salas_evento(db, total_pessoas, total_salas):
    lotacao_minima = db.session.query(func.min(SalaEvento.lotacao)).scalar()
    pessoas_por_sala = total_pessoas // total_salas
    limite = pessoas_por_sala
    id_pessoa = 1

    # Distribui igualmente as pessoas nas Salas de Evento
    salas = range(1, total_salas + 1)
    for sala in salas:
        while id_pessoa <= limite:
            pessoa = db.session.query(Pessoa).get_or_404(id_pessoa)
            pessoa.sala_evento_1 = sala
            pessoa.sala_evento_2 = troca_de_sala(sala, total_salas, id_pessoa)
            id_pessoa += 1
        limite += pessoas_por_sala
    
    # Distribui o "excedente" nas Salas de Evento não lotadas
    id_sala = 1
    while id_pessoa <= total_pessoas:
        pessoa = db.session.query(Pessoa).get_or_404(id_pessoa)
        id_sala = sala_nao_lotada(id_sala, lotacao_minima)
        pessoa.sala_evento_1 = id_sala
        pessoa.sala_evento_2 = id_sala
        id_sala += 1
        id_pessoa += 1

def atualiza_espacos_cafe(db, total_pessoas):
    menor_cafe = db.session.query(EspacoCafe).order_by(EspacoCafe.lotacao).first()
    maior_cafe = db.session.query(EspacoCafe).order_by(EspacoCafe.lotacao.desc()).first()
    metade_pessoas = total_pessoas // 2
    
    if metade_pessoas <= menor_cafe.lotacao:
        # Distribui metade das pessoas
        for i in range(1, metade_pessoas + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_1 = menor_cafe.id
            pessoa.espaco_cafe_2 = maior_cafe.id
        # Distribui outra metade das pessoas 
        for i in range(metade_pessoas + 1, total_pessoas + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_1 = maior_cafe.id
            pessoa.espaco_cafe_2 = menor_cafe.id
    else:
        # Distribui pessoas para o Primeiro Intervalo de Cafe
        for i in range(1, menor_cafe.lotacao + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_1 = menor_cafe.id
        for i in range(menor_cafe.lotacao + 1, total_pessoas + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_1 = maior_cafe.id
        # Distribui pessoas para o Segundo Intervalo de Cafe
        for i in range(1, total_pessoas - menor_cafe.lotacao + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_1 = maior_cafe.id
        for i in range(total_pessoas - menor_cafe.lotacao + 1, total_pessoas + 1):
            pessoa = db.session.query(Pessoa).get_or_404(i)
            pessoa.espaco_cafe_2 = menor_cafe.id

def atualiza_database(db):
    total_pessoas = db.session.query(Pessoa).count()
    total_salas = db.session.query(SalaEvento).count()
    total_cafes = db.session.query(EspacoCafe).count()
    
    if total_salas > 0 and total_cafes > 0:
        atualiza_salas_evento(db, total_pessoas, total_salas)
        atualiza_espacos_cafe(db, total_pessoas)

        try:
            db.session.commit()
        except:
            return 'Houve um problema na atualização do banco de dados'
