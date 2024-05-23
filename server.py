from src.domain.app import app, io
from src.routes import user_routes, apoiadores_routes
from src.domain.configs.database import base, engine
from src.models import Usuarios, Apoiadores, Admin

base.metadata.create_all(engine)

app.register_blueprint(user_routes)
app.register_blueprint(apoiadores_routes)


@app.get('/')
def index(*args):
    return {'Prof Validator': 'service runned withou any problem'}

def run_app(*args):
    io.run(
        app=app,
        debug=True,
        port=3100,
        host='0.0.0.0',
        allow_unsafe_werkzeug=True
    )

if __name__ == '__main__':
    run_app()

