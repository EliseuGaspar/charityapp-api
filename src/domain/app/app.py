from os import getenv
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flasgger import Swagger
from py_dotenv import read_dotenv

read_dotenv('.env')

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*":{"origins":"*"},r"/socket.io/*": {"origins": "*"}})
app.config['SECRET_KEY'] = getenv('secretKey')
app.config['SWAGGER'] = {
    'title': 'Care-Guiné API',
    'description': 'Documentação da API do ProfValidator'
}
Swagger(app = app)