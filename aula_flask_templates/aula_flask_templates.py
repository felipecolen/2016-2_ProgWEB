import datetime
import os, pymysql  # pip install PyMySql
from flask import Flask, request, redirect
# o request é para pegarmos os conteúdos passados no post/submit do formulário
# redirect -> para redirecionar depois do insert no banco
from flask.helpers import url_for  # para retornar para outra url a partir do seu controller

from flask.templating import render_template
# é necessário importar o render_template para separarmos os htmls

app = Flask(__name__)


# conexão mysql
conexao = pymysql.connect(
    host=os.getenv('IP', '0.0.0.0'),
    user='root',
    passwd='senhamysql',
    db='db_nome_do_db'
)
conexao_cursor = conexao.cursor()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])  # você pode definir várias urls para o mesmo método
def retorna_index():
    # por padrão, os templates tem que estar na pasta templates, mas você pode mudar isso
    return render_template('index.html')


@app.route('/contato', methods=['GET', 'POST'])
def cadastra_contato():

    if request.method == 'POST':
        nome = request.form['nome']
        msg = request.form['mensagem']
        data_e_hora = datetime.datetime.now()  # pega a data e hora atuais
        query_sql = "INSERT INTO tb_contato (nome, mensagem, data_envio) " \
                    "VALUES ('%s', '%s', '%s')" % (nome, msg, data_e_hora)
        conexao_cursor.execute(query_sql)  # executa o comando no banco
        conexao.commit()  # salva as alterações no banco

        return redirect(url_for('mensagens_contato'))  # redireciona para o controller retorna_index

    return render_template('contato.html')


@app.route('/mensagens', methods=['GET'])
def mensagens_contato():

    query_sql = "SELECT * FROM tb_contato"  # a query em SQL
    conexao_cursor.execute(query_sql)  # executa o comando no banco
    todas_mensagens = conexao_cursor.fetchall()

    return render_template('mensagens.html', mensagens=todas_mensagens)


if __name__ == '__main__':
    # inclua essas linhas para pegar a porta e o ip configurados no heroku ou c9 por exemplo
    porta = int(os.getenv('PORT', 5000))
    host = os.getenv('IP', '0.0.0.0')
    # lembre-se sempre de ativar o debug para visualizar melhor
    # os erros e reiniciar automaticamente seu servidor
    app.run(debug=True, port=porta, host=host)
