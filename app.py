import os
from flask import Flask, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Inicializar Flask
app = Flask(__name__ )
CORS(app)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Railway PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # SQLite local para desenvolvimento
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///splits_sequential.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco
db = SQLAlchemy(app)

# Importar modelos e rotas
from models import URLSplit
from routes import url_split_bp

# Registrar blueprints
app.register_blueprint(url_split_bp, url_prefix='/api')

# Rota principal
@app.route('/')
def index():
    try:
        with open('static/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return '<h1>URL Splitter Sequential V2</h1><p>Interface em desenvolvimento...</p>'

# Criar tabelas
with app.app_context():
    db.create_all()
    print("✅ Banco de dados inicializado")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
