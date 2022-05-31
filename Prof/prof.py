from datetime import date

from flask import render_template, request, Blueprint
from Prof.form import ProfForm
from __init__ import bd
from Prof.models import Professeur
from cours.models import CoursProf, Cour

profview_blueprint = Blueprint('profview_blueprint', __name__)




def getallprofactif():
    professeurs = Professeur.query.filter_by(prof_actif=1).all()
    return professeurs

def getallprofnonactif():
    professeurs = Professeur.query.filter_by(prof_actif="0").all()

    return professeurs

@profview_blueprint.route('/',methods= ['GET','POST'])
def profview():

    if "sort" in request.form:
        buttonvalue = request.form['sort']

        if buttonvalue == 'nom':
            profs = Professeur.query.filter_by(prof_actif=1).order_by("prof_nom").all()
            return render_template('Prof/prof.html', profs=profs)

        if buttonvalue == 'prenom':
            profs = Professeur.query.filter_by(prof_actif=1).order_by("prof_prenom").all()
            return render_template('Prof/prof.html', profs=profs)

        else:
            profs = getallprofactif()
            return render_template('Prof/prof.html', profs=profs)
    else:
        profs = getallprofactif()
        return render_template('Prof/prof.html', profs=profs)


@profview_blueprint.route('/add',methods= ['GET','POST'])

def profadd():
    form = ProfForm()
    listcol = Professeur.metadata.tables['professeur'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('prof_id','prof_actif')]
    listcol.extend([ 'cours'])
    today = date.today()
    if form.validate_on_submit():
        newprof = Professeur()
        for attr in listcol:
            if attr != "cours":
                setattr(newprof, attr, form[attr].data)
        if bool(Professeur.query.filter_by(prof_nom=newprof.prof_nom,prof_prenom=newprof.prof_prenom).one_or_none()) == False:
            print("existe pas dans DB ")
            for cour in form.cours.data:
                newCoursProf = CoursProf()
                newCoursProf.cour = cour
                newCoursProf.year = int(today.strftime('%Y'))
                newprof.cours.append(newCoursProf)
            bd.session.commit()
        else:
            print("Existe dans db")
        return render_template('index.html')
    return render_template('Prof/add.html', listcol=listcol, form=form)

@profview_blueprint.route('/update',methods= ['GET','POST'])
def profupdate():
    id = request.form['id']
    form = ProfForm(obj=Professeur.query.filter_by(prof_id=id).first())
    listcol = Professeur.metadata.tables['professeur'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('prof_id')]
    listcol.extend(['cours'])
    if form.validate_on_submit():
        newprof = Professeur()
        for attr in listcol:
            if attr != "cours":
                setattr(newprof, attr, form[attr].data)
        if bool(Professeur.query.filter_by(prof_nom=newprof.prof_nom,prof_prenom=newprof.prof_prenom).one_or_none()) == False:
            print("existe pas dans DB ")
            oldeleve = Professeur.query.filter_by(prof_id=id).first()
            for attr in listcol:
                if attr != "cours":
                    setattr(oldeleve, attr, form[attr].data)
                    print(attr)
                    bd.session.commit()
            print('cours ici ______')
            for cours in oldeleve.cours:
                bd.session.delete(cours)
            for cour in form.cours.data:
                newcoursprof = CoursProf()
                newcoursprof.cour = cour
                oldeleve.cours.append(newcoursprof)
            bd.session.commit()
        else:
            print("Existe dans db")
            print(newprof.eleve_nom, newprof.eleve_prenom)
        return render_template('index.html')
    else:
        student = Professeur.query.filter_by(prof_id=id).first()
        currentcours = []
        for i in student.cours:
            currentcours.append(i.cour)
        form = ProfForm(obj=Professeur.query.filter_by(prof_id=id).first())
        form.cours.data = currentcours
        bd.session.commit()
    return render_template('Prof/update.html', listcol=listcol, form=form, id=id)

@profview_blueprint.route('/coursprof',methods= ['GET','POST'])
def coursbyprof():
    """
    id=request.form['id']
    Prof= Professeur.query.filter_by(prof_id=id).first()
    return render_template('Prof/coursprof.html',prof=Prof)
    """
    id=request.form['id']
    today = date.today()
    todayyear = int(today.strftime('%Y'))
    prof = Professeur.query.filter_by(prof_id=id).first()
    listyear = bd.session.query(CoursProf.year).filter(CoursProf.prof_id == id).distinct()
    if "sort" in request.form:
        sort = request.form['id']
        buttonvalue = request.form['sort']
        cours = bd.session.query(Cour).join(CoursProf).filter(CoursProf.prof_id == id).filter(CoursProf.year == buttonvalue).all()
        listyear=sorted(listyear,reverse=True)
        return render_template('Prof/coursprof.html', cours=cours, listyear=listyear, sortyear=buttonvalue,prof=prof,sort=sort,year=buttonvalue)
    else:
        cours = bd.session.query(Cour).join(CoursProf).filter(CoursProf.prof_id == id).filter(CoursProf.year == todayyear).all()
        listyear=sorted(listyear,reverse=True)
        return render_template('Prof/coursprof.html', cours=cours, listyear=listyear,prof=prof,year=todayyear)

@profview_blueprint.route('/out',methods= ['GET','POST'])
def outprofesseur():
    id=request.form['id']
    prof= Professeur.query.filter_by(prof_id=id).first()
    prof.prof_actif='0'
    bd.session.commit()
    profs = getallprofactif()
    return render_template('Prof/prof.html',profs=profs)

@profview_blueprint.route('/in',methods= ['GET','POST'])
def inprofesseur():
    id=request.form['id']
    prof= Professeur.query.filter_by(prof_id=id).first()
    prof.prof_actif='1'
    bd.session.commit()
    profs = getallprofnonactif()
    return render_template('Prof/oldprof.html', profs=profs)


@profview_blueprint.route('/Archive',methods= ['GET','POST'])
def oldprofesseur():
    if "sort" in request.form:
        buttonvalue = request.form['sort']

        if buttonvalue == 'nom':
            profs = Professeur.query.filter_by(prof_actif="0").order_by("prof_nom").all()
            return render_template('Prof/oldprof.html', profs=profs)

        if buttonvalue == 'prenom':
            profs = Professeur.query.query.filter_by(prof_actif="0").order_by("prof_prenom").all()
            return render_template('Prof/oldprof.html', profs=profs)

        else:
            profs = Professeur.query.query.filter_by(prof_actif="0").all()
            return render_template('Prof/oldprof.html', profs=profs)
    else:
        profs = Professeur.query.filter_by(prof_actif="0").all()
        return render_template('Prof/oldprof.html', profs=profs)