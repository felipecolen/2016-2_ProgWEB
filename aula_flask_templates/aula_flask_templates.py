from flask import Flask
from flask.templating import render_template  # é necessário importar o render_template para separarmos os htmls

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    # lembre-se sempre de ativar o debug para visualizar melhor os erros e reiniciar automaticamente seu servidor
    app.run(debug=True)
