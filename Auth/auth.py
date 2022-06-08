from flask import Blueprint, render_template_string
from flask_security import auth_required
from __init__ import db,bd
from student.form import EleveForm
from student.models import Eleve
from cours.models import Courseleve
from datetime import date
authblueprint = Blueprint('authblueprint', __name__)


@authblueprint.route('/',methods= ['GET','POST'])
@auth_required()
def home():
    return render_template_string("Hello {{ current_user.email }}")