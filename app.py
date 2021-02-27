from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from classes import Pessoa, SalaEvento, EspacoCafe, Locais
from funcoes import atualiza_lotacao_real, calcula_lotacao_maxima, troca_de_sala, sala_nao_lotada, atualiza_database

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

@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    if request.method == 'POST':
        if 'consultar pessoa' in request.form:
            return redirect('/consulta-pessoa')
        elif 'consultar sala evento' in request.form:
            return redirect('/consulta-sala-evento')
        elif 'consultar espaco cafe' in request.form:
            return redirect('/consulta-espaco-cafe')
        elif 'voltar' in request.form:
            return redirect('/')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        atualiza_database(db)
        return render_template('consulta.html')

@app.route('/consulta-pessoa', methods=['POST', 'GET'])
def consulta_pessoa():
    if request.method == 'POST':
        if 'consultar' in request.form:
            id_pessoa = request.form['id_pessoa']
            return redirect(url_for('consulta_pessoa_selecionada', id_pessoa=id_pessoa))
        elif 'voltar' in request.form:
            return redirect('/consulta')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        pessoas = Pessoa.query.all()
        return render_template('consulta-pessoa.html', pessoas=pessoas)

@app.route('/consulta-pessoa-selecionada/<int:id_pessoa>', methods=['POST', 'GET'])
def consulta_pessoa_selecionada(id_pessoa):
    if request.method == 'POST':
        return redirect('/consulta-pessoa')
    else:
        pessoa = Pessoa.query.get_or_404(id_pessoa)
        locais = Locais(pessoa)
        return render_template('consulta-pessoa-selecionada.html', pessoa=pessoa, locais=locais)

@app.route('/consulta-sala-evento', methods=['POST', 'GET'])
def consulta_sala_evento():
    if request.method == 'POST':
        if 'consultar' in request.form:
            id_sala = request.form['id_sala_evento']
            return redirect(url_for('consulta_sala_evento_selecionada', id_sala=id_sala))
        elif 'voltar' in request.form:
            return redirect('/consulta')
        else:
            return 'Erro ao verificar requisição do usuário'
    else:
        salas_evento = SalaEvento.query.all()
        return render_template('consulta-sala-evento.html', salas_evento=salas_evento)

@app.route('/consulta-sala-evento-selecionada/<int:id_sala>', methods=['POST', 'GET'])
def consulta_sala_evento_selecionada(id_sala):
    if request.method == 'POST':
        return redirect('/consulta-sala-evento')
    else:
        sala = SalaEvento.query.get_or_404(id_sala)
        pessoas_etapa_1 = Pessoa.query.filter_by(sala_evento_1 = id_sala).all()
        pessoas_etapa_2 = Pessoa.query.filter_by(sala_evento_2 = id_sala).all()
        return render_template('consulta-sala-evento-selecionada.html', sala=sala, pessoas_etapa_1=pessoas_etapa_1, pessoas_etapa_2=pessoas_etapa_2)

@app.route('/consulta-espaco-cafe', methods=['POST', 'GET'])
def consulta_espaco_cafe():
    if request.method == 'POST':
        if 'consultar' in request.form:
            id_cafe = request.form['id_espaco_cafe']
            return redirect(url_for('consulta_espaco_cafe_selecionado', id_cafe=id_cafe))
        elif 'voltar' in request.form:
            return redirect('/consulta')
    else:
        espacos_cafe = EspacoCafe.query.all()
        return render_template('consulta-espaco-cafe.html', espacos_cafe=espacos_cafe)

@app.route('/consulta-espaco-cafe-selecionado/<int:id_cafe>', methods=['POST', 'GET'])
def consulta_espaco_cafe_selecionado(id_cafe):
    if request.method == 'POST':
        return redirect('/consulta-espaco-cafe')
    else:
        cafe = EspacoCafe.query.get_or_404(id_cafe)
        pessoas_etapa_1 = Pessoa.query.filter_by(espaco_cafe_1 = id_cafe).all()
        pessoas_etapa_2 = Pessoa.query.filter_by(espaco_cafe_2 = id_cafe).all()
        return render_template('consulta-espaco-cafe-selecionado.html', cafe=cafe, pessoas_etapa_1=pessoas_etapa_1, pessoas_etapa_2=pessoas_etapa_2)

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run(debug=True)
