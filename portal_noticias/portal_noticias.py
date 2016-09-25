import datetime
from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


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
    return render_template('noticias_todas.html', data_no_html=data_python, hora_no_html=hora_python)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
