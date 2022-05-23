from flask import Flask,render_template
from flask_bootstrap import Bootstrap

from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from config import *



db = MySQL()
bd = SQLAlchemy()
Base = declarative_base()
metadata = Base.metadata



def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)
    app.config.from_object(TestingConfig)

    db.init_app(app)
    bd.init_app(app)
    Bootstrap(app)
    from student.student import studentview_blueprint
    from cours.cours import coursview_blueprint
    from Prof.prof import profview_blueprint



    # Register blueprint(s)
    # app.register_blueprint(xyz_module)
    app.register_blueprint(studentview_blueprint,url_prefix='/student')
    app.register_blueprint(coursview_blueprint, url_prefix='/cours')
    app.register_blueprint(profview_blueprint, url_prefix='/prof')
    return app
