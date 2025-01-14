#!/bin/bash

# Create the project structure
mkdir -p plantswap/app/static plantswap/app/templates plantswap/migrations

# Add __init__.py
cat > ./app/__init__.py << 'EOF'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
EOF

# Add routes.py
cat > ./app/routes.py << 'EOF'
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')
EOF

# Add models.py
cat > ./app/models.py << 'EOF'
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
EOF

# Add forms.py
cat > ./app/forms.py << 'EOF'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
EOF

# Add run.py
cat > ./run.py << 'EOF'
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
EOF

# Add requirements.txt
cat > ./requirements.txt << 'EOF'
flask
sqlalchemy
flask-wtf
flask-bcrypt
flask-login
flask-migrate
EOF

echo "Setup complete! Your plantswap project is ready."
