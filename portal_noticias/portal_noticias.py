import datetime
import os
import pymysql
from flask import Flask, request, redirect, session
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)


conexao = pymysql.connect(
    host=os.getenv('IP', '172.17.0.3'),
    user='root',
    passwd='senhamysql',
    db='portal_flask'
)
conexao_cursor = conexao.cursor()


@app.route('/criar_tabela', methods=['GET'])
def criar_tabela():

    query_sql = """
        CREATE TABLE tb_usuario (
          id int(11) NOT NULL AUTO_INCREMENT,
          usuario varchar(20) NOT NULL,
          nome varchar(100) NOT NULL,
          senha varchar(60) NOT NULL,
          data_cadastro datetime NOT NULL,
          PRIMARY KEY (id)
        );
        CREATE TABLE noticia (
            id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
            titulo VARCHAR(100),
            noticia VARCHAR(500),
            data_post DATETIME
        );
        CREATE UNIQUE INDEX tb_usuario_id_uindex ON portal_flask.tb_usuario (id);
        CREATE UNIQUE INDEX tb_usuario_usuario_uindex ON portal_flask.tb_usuario (usuario);
        CREATE UNIQUE INDEX noticia_id_uindex ON portal_flask.noticia (id)
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabelas criadas com sucesso!!</h1>'


@app.route('/excluir_tabela', methods=['GET'])
def excluir_tabela():

    query_sql = """
        DROP TABLE portal_flask.tb_usuario;
        DROP TABLE portal_flask.noticia;
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabelas excluídas com sucesso!!</h1>'


@app.route('/usuarios/', methods=['GET'])
def ver_usuarios():

    # monta o select para pegar todos os registros
    codigo_sql = """
        SELECT * FROM tb_usuario
    """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em 'usuarios' todos os consultados no banco
    usuarios = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('usuarios/ver_usuarios.html', usuarios=usuarios)


@app.route('/usuarios/add', methods=['GET', 'POST'])
def cadastrar_usuario():

    # se clicou no botão "enviar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        data_cadastro = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO tb_usuario (usuario, nome, senha, data_cadastro)
            VALUES ('{}', '{}', '{}', '{}')
        """.format(usuario, nome, senha, data_cadastro)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os usuarios
        return redirect(url_for('ver_usuarios'))

    return render_template('usuarios/add_usuario.html')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    # se clicou no botão "atualizar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        data_cadastro = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            UPDATE tb_usuario
            SET usuario='{}', nome='{}', senha='{}', data_cadastro='{}'
            WHERE id='{}'
        """.format(usuario, nome, senha, data_cadastro, id)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os contatos
        return redirect(url_for('ver_usuarios'))

    # se não foi um post então consulta e mostra na página
    # monta o sql para consultar o registro pelo id
    codigo_sql = "SELECT * FROM tb_usuario WHERE id = {}".format(id)

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contato todos os consultados no banco
    usuario = conexao_cursor.fetchall()

    # mostra no template o contato[0], pois vem como uma lista contento 1 elemento apenas
    return render_template('usuarios/editar_usuario.html', usuario=usuario[0])


@app.route('/usuarios/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):

    # se clicou no botão "excluir"
    # monta o código sql para excluir se for o ID tal...
    codigo_sql = "DELETE FROM tb_usuario WHERE id={}".format(id)

    conexao_cursor.execute(codigo_sql)  # executa no banco
    conexao.commit()

    # redireciona para a página com todos os usuarios
    return redirect(url_for('ver_usuarios'))


@app.route('/acessar', methods=['GET', 'POST'])
def acessar():
    if 'usuario' in session:
        usuario = session['usuario']
    else:
        usuario = 'Não logado'

    if request.method == 'POST':

        usuario_digitado = request.form['usuario']
        senha_digitada = request.form['senha']

        # se for um método post, vamos pegar o usuário e senha digitados
        # e pesquisar no banco se existe esse usuário
        codigo_sql = "SELECT * FROM tb_usuario WHERE usuario = '{}'".format(usuario_digitado)

        # executo o sql montado acima
        conexao_cursor.execute(codigo_sql)

        # pego o resultado dessa consulta
        tem_cadastro = conexao_cursor.fetchall()  # lembrando que vem uma "LISTA"

        # agora, verifico se tem algum registro
        if tem_cadastro:
            # se tem, então eu pego o primeiro e único elemento da lista
            dados_usuario_banco = tem_cadastro[0]

            # se tem, então comparamos a senha digitada com a senha salva
            # lembrando que, na posição [0] vem o ID, na [1] o usuário...
            # na [3] a senha
            if dados_usuario_banco[3] == senha_digitada:
                # se chegou aqui, então a senha tá certa
                # crio uma sessão com o nome do usuário
                # e automaticamente vai criar um cookie seguro
                session['usuario'] = dados_usuario_banco[1]
                return redirect(url_for('logado_sessao'))

    return render_template('acessar.html', usuario=usuario)


# lembrando que é preciso criar uma chave secreta para seu projeto
# essa chave será usada para gerar um código criptografado no cookie
app.secret_key = 'umachavesecretaTIPOHASH000lhdjsahkjsahdkjhahdlkjxyczuy'


@app.route('/logado_sessao/', methods=['GET', 'POST'])
def logado_sessao():

    # para saber se o usuário e a senha foram inseridos corretamente
    # verificamos se existe o usuário na sessão
    if 'usuario' in session:
        return '<h1>logado com sucesso - utilizando sessões <br>' \
               ' Usuário: {}</h1>'.format(session['usuario'])


@app.route('/encerrar_sessao')
def encerrar_sessao():
    # remove o usuário logado da sessão atual
    session.pop('usuario', None)
    return redirect(url_for('acessar'))



@app.route('/')
def index():
    data_python = datetime.datetime.now().date().strftime('%d/%m/%Y')
    hora_python = datetime.datetime.now().time().strftime('%H:%m:%S')
    return render_template('index.html', data_no_html=data_python, hora_no_html=hora_python)


@app.route('/noticias')
def mostrar_noticias():
    data_e_hora = datetime.datetime.now()
    data_python = data_e_hora.date().strftime('%d/%m/%Y')
    hora_python = data_e_hora.time().strftime('%Hh %mmin %Ss')

    conexao_cursor.execute("SELECT * FROM noticia;")
    noticias = conexao_cursor.fetchall()

    return render_template('noticias.html', data_no_html=data_python, hora_no_html=hora_python,
                           noticias=noticias)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':
        titulo = request.form['titulo']
        noticia = request.form['noticia']
        # a data no form fica para o usuário ver no formato BR dd/mm/YYYY
        # mas pro banco, ajustamos para o padrão YYYY-mm-dd
        data_do_form = request.form['data_post'].split('/')
        data_ajustada_db = '{}-{}-{}'.format(data_do_form[2], data_do_form[1], data_do_form[0])

        query = "INSERT INTO noticia (titulo, noticia, data_post) " \
                "VALUES ('%s', '%s', '%s')" % (titulo, noticia, data_ajustada_db)
        conexao_cursor.execute(query)
        conexao.commit()
        return redirect(url_for('index'))

    return render_template('cadastrar_noticia.html')


if __name__ == '__main__':
    host_c9 = os.getenv('IP', '0.0.0.0')
    porta_c9 = int(os.getenv('PORT', 5000))
    app.run(debug=True, host=host_c9, port=porta_c9)
