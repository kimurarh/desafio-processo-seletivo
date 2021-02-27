from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from classes import Pessoa, SalaEvento, EspacoCafe, Locais
from funcoes import atualiza_lotacao_real, calcula_lotacao_maxima

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
app.config['SQLALCHEMY_BINDS'] = {'salasevento': 'sqlite:///salasevento.db', 'espacoscafe': 'sqlite:///espacoscafe.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': 
        if 'cadastrar' in request.form:
            return redirect('/cadastro')
        elif 'consultar' in request.form:
            return redirect('/consulta')
        else:
            return 'Erro ao tentar acessar painel de cadastro/consulta'
    else:
        return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        if 'cadastrar pessoa' in request.form:
            return redirect('/cadastro-pessoa')
        elif 'cadastrar sala evento' in request.form:
            return redirect('/cadastro-sala-evento')
        elif 'cadastrar espaco cafe' in request.form:
            return redirect('/cadastro-espaco-cafe')
        elif 'voltar' in request.form:
            return redirect('/')
        else:
            return 'Erro ao acessar opções de cadastro'
    else:
        return render_template('cadastro.html')

@app.route('/cadastro-pessoa', methods=['POST', 'GET'])
def cadastro_pessoa():
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            pessoa_nome = request.form['nome']
            pessoa_sobrenome = request.form['sobrenome']
            nova_pessoa = Pessoa(nome=pessoa_nome, sobrenome=pessoa_sobrenome)
            if pessoa_nome == '' or pessoa_sobrenome == '':
                flash('Por favor, preencha todos os campos', 'erro')
                return redirect('/cadastro-pessoa')
            else:
                try:
                    db.session.add(nova_pessoa)
                    db.session.commit()
                    flash('{} {} cadastrado(a) com sucesso'.format(nova_pessoa.nome, nova_pessoa.sobrenome), 'sucesso')
                    return redirect('/cadastro-pessoa')
                except:
                    db.session.rollback()
                    return 'Houve um problema ao cadastrar a pessoa'
        elif 'voltar' in request.form:
            return redirect('/cadastro')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        total_pessoas = db.session.query(Pessoa).count()
        salas = db.session.query(SalaEvento).all()
        cafes = db.session.query(EspacoCafe).all()
        lotacao_maxima = calcula_lotacao_maxima(salas, cafes)
        print(lotacao_maxima)
        return render_template('cadastro-pessoa.html', num_salas=len(salas), num_cafes=len(cafes), lotacao_maxima=lotacao_maxima, total_pessoas=total_pessoas)

@app.route('/cadastro-sala-evento', methods=['POST', 'GET'])
def cadastro_sala_evento():
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            sala_nome = request.form['nome']
            sala_lotacao = request.form['lotacao']
            nova_sala_evento = SalaEvento(nome=sala_nome, lotacao=sala_lotacao)
            if sala_nome == '' or sala_lotacao == '':
                flash('Por favor, preencha todos os campos', 'erro')
                return redirect('/cadastro-sala-evento')
            else:
                try:
                    db.session.add(nova_sala_evento)
                    db.session.commit()
                    flash('{} cadastrada com sucesso'.format(nova_sala_evento.nome), 'sucesso')
                    return redirect('/cadastro-sala-evento')
                except:
                    db.session.rollback()
                    return 'Houve um problema ao cadastrar a sala de evento'
        elif 'voltar' in request.form:
            return redirect('/cadastro')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        salas = db.session.query(SalaEvento).all()
        atualiza_lotacao_real(db, salas)
        return render_template('cadastro-sala-evento.html', salas=salas)

@app.route('/cadastro-espaco-cafe', methods=['POST', 'GET'])
def cadastro_espaco_cafe():
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            cafe_nome = request.form['nome']
            cafe_lotacao = request.form['lotacao']
            novo_cafe = EspacoCafe(nome=cafe_nome, lotacao=cafe_lotacao)
            if cafe_nome == '' or cafe_lotacao == '':
                flash('Por favor, preencha todos os campos', 'erro')
                return redirect('/cadastro-espaco-cafe')
            else:
                try:
                    db.session.add(novo_cafe)
                    db.session.commit()
                    flash('{} cadastrado com sucesso'.format(novo_cafe.nome), 'sucesso')
                    return redirect('/cadastro-espaco-cafe')
                except:
                    db.session.rollback()
                    return 'Houve um problema ao cadastrar o espaco de cafe'
        elif 'voltar' in request.form:
            return redirect('/cadastro')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        num_cafes = EspacoCafe.query.count()
        return render_template('cadastro-espaco-cafe.html', num_cafes=num_cafes)

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run(debug=True)
