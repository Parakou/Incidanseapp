from flask import render_template, request, Blueprint
from __init__ import db,bd
from student.form import EleveForm
from student.models import Eleve
from cours.models import Courseleve
from datetime import date



studentview_blueprint = Blueprint('studentview_blueprint', __name__)

@studentview_blueprint.route('/',methods= ['GET','POST'])

def studentview():

    if "sort" in request.form:
        buttonvalue = request.form['sort']
        if buttonvalue == 'nom':
            eleve = Eleve.query.filter_by(eleve_actif=1).order_by("eleve_nom").all()
            return render_template('student/student.html', eleve=eleve)

        if buttonvalue == 'prenom':
            eleve = Eleve.query.filter_by(eleve_actif=1).order_by("eleve_prenom").all()
            return render_template('student/student.html', eleve=eleve)

        if buttonvalue == 'age':
            eleve = Eleve.query.filter_by(eleve_actif=1).order_by("eleve_age").all()
            return render_template('student/student.html', eleve=eleve)

        if buttonvalue == 'heuredecours':
            eleve = Eleve.query.filter_by(eleve_actif=1).order_by("eleve_heure").all()
            return render_template('student/student.html', eleve=eleve)

        else:
            eleve = Eleve.query.filter_by(eleve_actif=1).all()
            return render_template('student/student.html', eleve=eleve)
    else:
        eleve= Eleve.query.filter_by(eleve_actif=1).all()
        return render_template('student/student.html', eleve=eleve)

@studentview_blueprint.route('/search',methods= ['GET','POST'])
def search():
    searchlist=request.form['search']
    searchlist=searchlist.split()
    listcol=["eleve_prenom","eleve_nom","eleve_age","eleve_adresse","eleve_GSM","eleve_fixe","eleve_mail","eleve_mail2","ville_nom"]
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
    searchquery="select * from Eleve  inner join  Ville on Ville_id_Ville=ville_ID where eleve_actif=1 and"+" "+querysearch
    cur.execute(searchquery)
    eleve= cur.fetchall()
    return render_template('student/student.html', eleve=eleve)

@studentview_blueprint.route('/add',methods= ['GET','POST'])

def studentadd():
    form=EleveForm()
    """
    form=EleveForm(obj=Eleve.query.filter_by(eleve_prenom="John").first())
    studenttest=Eleve.query.filter_by(eleve_prenom="John").first()
    print(studenttest.cours)
    toadlist=[]
    for i in studenttest.cours:
       toadlist.append(i.cour)
    form.cours.data=toadlist
    """
    listcol=Eleve.metadata.tables['eleve'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('eleve_id', 'eleve_courst','eleve_nom_prenom','eleve_heure','eleve_actif','Ville_id_Ville','eleve_age')]
    listcol.extend(['ville', 'cours'])
    if form.validate_on_submit():
        neweleve=Eleve()
        for attr in listcol:
            if attr!="cours":
                setattr(neweleve,attr,form[attr].data)
        neweleve.Ville_id_Ville=form.ville.data.ville_ID
        today=date.today()
        neweleve.eleve_age=today.year - neweleve.eleve_datenaissance.year - ((today.month,today.day) < (neweleve.eleve_datenaissance.month,neweleve.eleve_datenaissance.day))
        if bool(Eleve.query.filter_by(eleve_nom=neweleve.eleve_nom,eleve_prenom=neweleve.eleve_prenom).one_or_none())==False:
            print("existe pas dans DB ")
            for cour in form.cours.data:
                newcourseleve=Courseleve()
                newcourseleve.cour=cour
                neweleve.cours.append(newcourseleve)
            bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('student/add.html',listcol=listcol, form=form)

@studentview_blueprint.route('/coursbystudent',methods= ['GET','POST'])
def coursbystudent():
    id=request.form['id']
    eleve= Eleve.query.filter_by(eleve_id=id).first()
    return render_template('student/courstudent.html',row=eleve)

@studentview_blueprint.route('/update',methods= ['GET','POST'])
def studentupdate():
    id = request.form['id']
    form = EleveForm(obj=Eleve.query.filter_by(eleve_id=id).first())
    listcol = Eleve.metadata.tables['eleve'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in (
    'eleve_id', 'eleve_courst', 'eleve_nom_prenom', 'eleve_heure', 'eleve_actif', 'Ville_id_Ville', 'eleve_age')]
    listcol.extend(['ville', 'cours'])
    if form.validate_on_submit():
        neweleve = Eleve()
        for attr in listcol:
            if attr != "cours":
                setattr(neweleve, attr, form[attr].data)
        neweleve.Ville_id_Ville = form.ville.data.ville_ID
        if bool(Eleve.query.filter_by(eleve_nom=neweleve.eleve_nom,eleve_prenom=neweleve.eleve_prenom).one_or_none()) == False:
            print("existe pas dans DB ")
            oldeleve = Eleve.query.filter_by(eleve_id=id).first()
            oldeleve.Ville_id_Ville = form.ville.data.ville_ID
            today = date.today()
            oldeleve.eleve_age = today.year - neweleve.eleve_datenaissance.year - ((today.month, today.day) < (
            neweleve.eleve_datenaissance.month, neweleve.eleve_datenaissance.day))
            print(oldeleve.cours)
            for attr in listcol:
                if attr != "cours":
                    setattr(oldeleve, attr, form[attr].data)
                    print(attr)
                    bd.session.commit()
            print('cours ici ______')
            for cours in oldeleve.cours:
                bd.session.delete(cours)
            for cour in form.cours.data:
                newcourseleve = Courseleve()
                newcourseleve.cour = cour
                oldeleve.cours.append(newcourseleve)
            bd.session.commit()
        else:
            print("Existe dans db")
            print(neweleve.eleve_nom, neweleve.eleve_prenom)
        return render_template('index.html')
    else:
        student = Eleve.query.filter_by(eleve_id=id).first()
        currentcours = []
        for i in student.cours:
            currentcours.append(i.cour)
        form = EleveForm(obj=Eleve.query.filter_by(eleve_id=id).first())
        form.cours.data = currentcours
        form.ville.data = student.Ville
        bd.session.commit()
    return render_template('student/update.html', listcol=listcol, form=form, id=id)

@studentview_blueprint.route('/studentout',methods= ['GET','POST'])
def outstudent():
    id=request.form['id']
    eleve= Eleve.query.filter_by(eleve_id=id).first()
    eleve.eleve_actif="0"
    bd.session.commit()
    return render_template('student/student.html')
