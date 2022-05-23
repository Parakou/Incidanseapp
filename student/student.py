from flask import render_template, request, Blueprint
from __init__ import db,bd
from student.models import Eleve
from ville.models import Ville,Province

studentview_blueprint = Blueprint('studentview_blueprint', __name__)







@studentview_blueprint.route('/',methods= ['GET','POST'])

def studentview():

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

        if buttonvalue == 'age':
            cur = db.connection.cursor()
            cur.execute("select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_age")
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)

        if buttonvalue == 'heuredecours':
            cur = db.connection.cursor()
            cur.execute("select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_heure ")
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)

        else:
            cur = db.connection.cursor()
            cur.execute(
                "select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_nom ")
            eleve = cur.fetchall()
            return render_template('student/student.html', eleve=eleve)

    else:
        list =Eleve.query.filter_by(eleve_nom='Rambo7').first()
        print(list.eleve_nom,list.eleve_nom,list.Ville.Ville_nom)
        cur = db.connection.cursor()
        cur.execute("select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1  order by eleve_nom ")
        eleve = cur.fetchall()
        return render_template('student/student.html', eleve=eleve)

@studentview_blueprint.route('/search',methods= ['GET','POST'])
def search():
    searchlist=request.form['search']
    searchlist=searchlist.split()
    listcol=["eleve_prenom","eleve_nom","eleve_age","eleve_adresse","eleve_GSM","eleve_fixe","eleve_mail","eleve_mail2","Ville_nom"]
    querysearch=""
    lasts=searchlist[-1]
    lastc=listcol[-1]
    for item in searchlist:
        for col in listcol:
            sfilter = " (" + col + " LIKE '%" + item + "%')"
            querysearch+=sfilter
            if (item == lasts) and (col == lastc):
                querysearch
            else:
                querysearch+=" or "

    cur=db.connection.cursor()
    searchquery="select * from Eleve  inner join  Ville on Ville_id_Ville=Ville_ID where eleve_actif=1 and"+" "+querysearch
    cur.execute(searchquery)
    eleve= cur.fetchall()
    return render_template('student/student.html', eleve=eleve)

@studentview_blueprint.route('/add',methods= ['GET','POST'])

def studentadd():
    listev=Ville.query.all()
    return render_template('student/add.html', listeville=listev)

@studentview_blueprint.route('/addstudent',methods= ['GET','POST'])

def addstudent():
    villid = Ville.query.filter_by(Ville_nom=request.form['ville']).first()
    neweleve= Eleve(eleve_nom=request.form['name'],eleve_prenom=request.form['firstname'],Ville=villid)
    bd.session.add(neweleve)
    bd.session.commit()
    return render_template('index.html')






