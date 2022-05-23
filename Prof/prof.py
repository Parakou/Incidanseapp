from flask import render_template, request, Blueprint
from __init__ import db,bd
from Prof.models import Prof
from ville.models import Ville,Province

profview_blueprint = Blueprint('profview_blueprint', __name__)




@profview_blueprint.route('/',methods= ['GET','POST'])

def profview():

    if "sort" in request.form:
        buttonvalue = request.form['sort']

        if buttonvalue == 'nom':
            cur = db.connection.cursor()
            cur.execute("select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_nom ")
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)

        if buttonvalue == 'prenom':
            cur = db.connection.cursor()
            x="select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_prenom"
            cur.execute(x)
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)


        else:
            cur = db.connection.cursor()
            cur.execute(
                "select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_nom ")
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)

    else:
        profs = Prof.query.all()
        return render_template('Prof/prof.html', profs=profs)