from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from webdata.config import Config

app = Flask(__name__)
this_config = Config()
app.config.from_object(Config)

app.config['SECRET_KEY'] = this_config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = this_config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = this_config.UPLOAD_FOLDER
db = SQLAlchemy() 
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

from webdata.main.routes import main
app.register_blueprint(main)