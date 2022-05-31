from flask import render_template, request, Blueprint
from Prof.form import ProfForm
from __init__ import bd
from Prof.models import Professeur
from cours.models import CoursProf


profview_blueprint = Blueprint('profview_blueprint', __name__)


@profview_blueprint.route('/',methods= ['GET','POST'])

def profview():

    if "sort" in request.form:
        buttonvalue = request.form['sort']

        if buttonvalue == 'nom':
            profs = Professeur.query.order_by("prof_nom").all()
            return render_template('Prof/prof.html', profs=profs)

        if buttonvalue == 'prenom':
            profs = Professeur.query.order_by("prof_prenom").all()
            return render_template('Prof/prof.html', profs=profs)

        else:
            profs = Professeur.query.all()
            return render_template('Prof/prof.html', profs=profs)
    else:
        profs= Professeur.query.all()
        return render_template('Prof/prof.html', profs=profs)

@profview_blueprint.route('/add',methods= ['GET','POST'])

def profadd():
    form = ProfForm()
    listcol = Professeur.metadata.tables['professeur'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('prof_id')]
    listcol.extend([ 'cours'])
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
                newprof.cours.append(newCoursProf)
            bd.session.commit()
        else:
            print("Existe dans db")
        return render_template('index.html')
    return render_template('Prof/add.html', listcol=listcol, form=form)

@profview_blueprint.route('/update',methods= ['GET','POST'])
def profupdate():
    """
    id = request.form['id']
    form=ProfForm(obj=Professeur.query.filter_by(prof_id=id).first())
    listcol=Professeur.metadata.tables['professeur'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('prof_id','prof_nom_prenom')]
    if form.validate_on_submit():
        newprof=Professeur()
        for attr in listcol:
            setattr(newprof, attr, form[attr].data)
        if bool(Professeur.query.filter_by(prof_nom=newprof.prof_nom,prof_prenom=newprof.prof_prenom).one_or_none()) == False:
            print("existe pas dans DB ")
            oldprof=Professeur.query.filter_by(prof_id=id).first()
            for attr in listcol:
                setattr(oldprof, attr, form[attr].data)
                bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('Prof/update.html',listcol=listcol, form=form, id=id)
    """
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
    id=request.form['id']
    Prof= Professeur.query.filter_by(prof_id=id).first()
    return render_template('Prof/coursprof.html',prof=Prof)