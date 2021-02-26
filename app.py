from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from classes import Pessoa, SalaEvento, EspacoCafe, Locais

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
        return render_template('cadastro-pessoa.html')

@app.route('/cadastro-sala-evento', methods=['POST', 'GET'])
def cadastro_sala_evento():
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            sala_nome = request.form['nome']
            sala_lotacao = request.form['lotacao']
            nova_sala_evento = SalaEvento(nome=sala_nome, lotacao=sala_lotacao)
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
        return render_template('cadastro-sala-evento.html')

@app.route('/cadastro-espaco-cafe', methods=['POST', 'GET'])
def cadastro_espaco_cafe():
    if request.method == 'POST':
        if 'cadastrar' in request.form:
            cafe_nome = request.form['nome']
            cafe_lotacao = request.form['lotacao']
            novo_cafe = EspacoCafe(nome=cafe_nome, lotacao=cafe_lotacao)
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
        return render_template('cadastro-espaco-cafe.html')

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run(debug=True)
