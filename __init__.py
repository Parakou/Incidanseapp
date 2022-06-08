from flask import Flask, render_template, session, url_for
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone

from flask_navigation import Navigation
from flask_security import Security, SQLAlchemyUserDatastore, login_required, \
    UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

from config import *



bd = SQLAlchemy()
nav = Navigation()
dropzone = Dropzone()
babel = Babel()

def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    babel.init_app(app)

    bd.init_app(app)
    Bootstrap(app)
    nav.init_app(app)
    dropzone.init_app(app)


    from cours.models import Cour,CoursProf,Courseleve
    from student.models import Eleve
    from Prof.models import Professeur
    from  Security.models import User,Role
    from ville.models import Province,Ville
    from Costume.models import Costume,Categorie,Rescost,Reservation

    from Costume.costume import costume_blueprint
    from cours.cours import coursview_blueprint
    from Prof.prof import profview_blueprint
    from student.student import studentview_blueprint
    user_datastore = SQLAlchemyUserDatastore(bd, User, Role)



    # Register blueprint(s)
    # app.register_blueprint(xyz_module)
    app.register_blueprint(studentview_blueprint,url_prefix='/student')
    app.register_blueprint(coursview_blueprint, url_prefix='/cours')
    app.register_blueprint(profview_blueprint, url_prefix='/prof')
    app.register_blueprint(costume_blueprint,url_prefix='/costume')
    return app
