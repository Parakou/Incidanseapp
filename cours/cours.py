from flask import render_template, request, Blueprint
from __init__ import db,bd
from student.models import Eleve
from cours.models import Cour,Courseleve
from student.models import Eleve

coursview_blueprint = Blueprint('coursview_blueprint', __name__)


@coursview_blueprint.route('/',methods= ['GET','POST'])
def courview():
        cours=Cour.query.all()
        studentbycours()
        return render_template('Cours/cours.html', cours=cours)

def studentbycours():
    Courtest=Eleve.query.filter_by(eleve_id=1).first()
    tag = Courtest.participant
    for y  in tag:
        print(y.Cours_nom)
    #Coursbystudent=Cour.query.with_parent(tag)
    #print(Coursbystudent)
    return