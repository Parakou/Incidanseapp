from flask import render_template, request, Blueprint
from flask_security import roles_accepted
from sqlalchemy import func

from __init__ import bd
from student.form import EleveForm
from student.models import Eleve
from cours.models import Courseleve, Cour
from datetime import date



studentview_blueprint = Blueprint('studentview_blueprint', __name__)


def getallstudentactif():
    eleve = Eleve.query.filter_by(eleve_actif=1).all()
    return eleve

def getallstudentnonactif():
    eleve = Eleve.query.filter_by(eleve_actif="0").all()
    return eleve

@studentview_blueprint.route('/',methods= ['GET','POST'])
def studentview():
        eleve =getallstudentactif()
        return render_template('student/student.html', eleve=eleve)


@studentview_blueprint.route('/add',methods= ['GET','POST'])
@roles_accepted('Admin')
def studentadd():
    form=EleveForm()
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
                newcourseleve.year=int(today.strftime('%Y'))
                newcourseleve.cour=cour
                neweleve.cours.append(newcourseleve)
            bd.session.commit()
            neweleve.eleve_heure = bd.session.query(func.sum(Cour.Cours_temps)).join(Courseleve).filter(Courseleve.eleve_eleve_id == neweleve.eleve_id).all()
            bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('student/add.html',listcol=listcol, form=form)

@studentview_blueprint.route('/coursbystudent',methods= ['GET','POST'])
def coursbystudent():
    """
    id=request.form['id']
    eleve= Eleve.query.filter_by(eleve_id=id).first()
    return render_template('student/courstudent.html',row=eleve)
    """
    id=request.form['id']
    today = date.today()
    todayyear = int(today.strftime('%Y'))
    eleve = Eleve.query.filter_by(eleve_id=id).first()
    listyear = bd.session.query(Courseleve.year).filter(Courseleve.eleve_eleve_id == id).distinct()
    if "sort" in request.form:
        sort = request.form['id']
        buttonvalue = request.form['sort']
        cours = bd.session.query(Cour).join(Courseleve).filter(Courseleve.eleve_eleve_id == id).filter(Courseleve.year == buttonvalue).all()
        listyear=sorted(listyear,reverse=True)
        return render_template('student/courstudent.html', cours=cours, listyear=listyear, sortyear=buttonvalue,eleve=eleve,sort=sort,year=buttonvalue)
    else:
        cours = bd.session.query(Cour).join(Courseleve).filter(Courseleve.eleve_eleve_id == id).filter(Courseleve.year == todayyear).all()
        listyear=sorted(listyear,reverse=True)
        return render_template('student/courstudent.html', cours=cours, listyear=listyear,eleve=eleve,year=todayyear)

@studentview_blueprint.route('/update',methods= ['GET','POST'])
def studentupdate():
    id = request.form['id']
    form = EleveForm(obj=Eleve.query.filter_by(eleve_id=id).first())
    listcol = Eleve.metadata.tables['eleve'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in (
    'eleve_id', 'eleve_courst', 'eleve_nom_prenom', 'eleve_heure', 'eleve_actif', 'Ville_id_Ville', 'eleve_age')]
    listcol.extend(['ville', 'cours'])
    today = date.today()
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
            oldeleve.eleve_age = today.year - neweleve.eleve_datenaissance.year - ((today.month, today.day) < (neweleve.eleve_datenaissance.month, neweleve.eleve_datenaissance.day))
            for attr in listcol:
                if attr != "cours":
                    setattr(oldeleve, attr, form[attr].data)
                    bd.session.commit()
            print('cours ici ______')
            for cours in oldeleve.cours:
                if cours.year==today.year:
                    bd.session.delete(cours)
            for cour in form.cours.data:
                newcourseleve = Courseleve()
                newcourseleve.cour = cour
                newcourseleve.year = int(today.strftime('%Y'))
                oldeleve.cours.append(newcourseleve)
            bd.session.commit()
            oldeleve.eleve_heure = bd.session.query(func.sum(Cour.Cours_temps)).join(Courseleve).filter(Courseleve.eleve_eleve_id == oldeleve.eleve_id).filter(Courseleve.year ==today.year).all()
            bd.session.commit()
        else:
            print("Existe dans db")
            print(neweleve.eleve_nom, neweleve.eleve_prenom)
        return render_template('index.html')
    else:
        student = Eleve.query.filter_by(eleve_id=id).first()
        currentcours = []
        for i in student.cours:
            if i.year==today.year:
                currentcours.append(i.cour)
        form = EleveForm(obj=Eleve.query.filter_by(eleve_id=id).first())
        form.cours.data = currentcours
        form.ville.data = student.Ville
        bd.session.commit()
    return render_template('student/update.html', listcol=listcol, form=form, id=id)

@studentview_blueprint.route('/out',methods= ['GET','POST'])
def outstudent():
    id=request.form['id']
    eleve= Eleve.query.filter_by(eleve_id=id).first()
    eleve.eleve_actif='0'
    bd.session.commit()
    eleve = getallstudentactif()
    return render_template('student/student.html',eleve=eleve)

@studentview_blueprint.route('/in',methods= ['GET','POST'])
def instudent():
    id=request.form['id']
    eleve= Eleve.query.filter_by(eleve_id=id).first()
    eleve.eleve_actif='1'
    bd.session.commit()
    eleve = getallstudentnonactif()
    return render_template('student/oldstudent.html', eleve=eleve)

@studentview_blueprint.route('/ancien',methods= ['GET','POST'])
def oldstudent():
    eleve = getallstudentnonactif()
    return render_template('student/oldstudent.html', eleve=eleve)
