from flask import Flask
from flask.templating import render_template  # é necessário importar o render_template para separarmos os htmls

app = Flask(__name__)


@app.route('/')
@app.route('/index')  # você pode definir várias urls para o mesmo método
def hello_world():
    # antes fizemos assim
    # return 'Hello um texto qualquer com ou sem <h1>Html</h1>'

    # agora só alteramos o retorno incluindo o render template
    # por padrão, os templates tem que estar na pasta templates
    return render_template('index.html')


if __name__ == '__main__':
    # lembre-se sempre de ativar o debug para visualizar melhor os erros e reiniciar automaticamente seu servidor
    app.run(debug=True)
