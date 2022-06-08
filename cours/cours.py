from datetime import date

from flask import render_template, request, Blueprint, make_response
import pdfkit

from Prof.models import Professeur
from __init__ import bd
from cours.models import Cour, Courseleve, CoursProf
from student.models import Eleve
from cours.form import Courform

wkhtmltopdf_options = {
    #'enable-local-file-access': True,
}

coursview_blueprint = Blueprint('coursview_blueprint', __name__)


@coursview_blueprint.route('/',methods= ['GET','POST'])
def courview():
        cours=Cour.query.filter_by(Cours_actif=1).all()
        return render_template('Cours/cours.html', cours=cours)

@coursview_blueprint.route('/anciencour',methods= ['GET','POST'])
def courold():
        cours=Cour.query.filter_by(Cours_actif="0").all()
        return render_template('Cours/cours.html', cours=cours)

@coursview_blueprint.route('/add',methods= ['GET','POST'])
def couradd():
    form=Courform()
    listcol=Cour.metadata.tables['cour'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('Cours_id','Cours_actif')]
    print(request.form.get("submitbutton"))
    if request.form.get("submitbutton") == "Envoyer":
        print("top")
        if form.validate_on_submit():
            print("top top ")
            newcour=Cour()
            for attr in listcol:
                setattr(newcour, attr, form[attr].data.capitalize())
            if bool(Cour.query.filter_by(Cours_nom=newcour.Cours_nom, Cours_jours=newcour.Cours_jours).one_or_none())==False:
                print("existe pas dans DB ")
                bd.session.add(newcour)
                bd.session.commit()
                return render_template('index.html')
        else:
            print("Existe dans db")
            return render_template('Cours/add.html',listcol=listcol, form=form)

    return render_template('Cours/add.html',listcol=listcol, form=form)

@coursview_blueprint.route('/studentbycour',methods= ['GET','POST'])
def studentbycours():
    id=request.form['id']
    today = date.today()
    todayyear = int(today.strftime('%Y'))
    listyear = bd.session.query(Courseleve.year).filter(Courseleve.Cours_Coursid == id).distinct()
    cour = Cour.query.filter_by(Cours_id=id).first()
    if "sort" in request.form:
        buttonvalue = request.form['sort']
        eleves = bd.session.query(Eleve).join(Courseleve).filter(Courseleve.Cours_Coursid == id).filter(Courseleve.year == buttonvalue).filter(Eleve.eleve_actif == 1).all()
        profs=bd.session.query(Professeur).join(CoursProf).filter(CoursProf.prof_id == id).filter(CoursProf.year == buttonvalue).all()
        for i in profs:
            print(i.prof_id,i.prof_nom)
        listyear=sorted(listyear,reverse=True)
        return render_template('Cours/studentcour.html', eleves=eleves, cour=cour, listyear=listyear,sortyear=buttonvalue,profs=profs)
    else:
        eleves=bd.session.query(Eleve).join(Courseleve).filter(Courseleve.Cours_Coursid==id).filter(Courseleve.year==todayyear).filter(Eleve.eleve_actif==1).all()
        profs = bd.session.query(Professeur).join(CoursProf).filter(CoursProf.prof_id == id).filter(CoursProf.year == todayyear).all()
        listyear=sorted(listyear,reverse=True)
        for i in profs:
            print(i.prof_id, i.prof_nom)
        return render_template('Cours/studentcour.html',eleves=eleves,cour=cour,listyear=listyear,currentyear=todayyear,profs=profs)

@coursview_blueprint.route('/update',methods= ['GET','POST'])
def courupdate():
    id = request.form['id']
    form=Courform(obj=Cour.query.filter_by(Cours_id=id).first())
    listcol=Cour.metadata.tables['cour'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('Cours_id','Cours_actif')]
    if form.validate_on_submit():
        newcour=Cour()
        for attr in listcol:
            setattr(newcour, attr, form[attr].data)
        if bool(Cour.query.filter_by(Cours_nom=newcour.Cours_nom, Cours_jours=newcour.Cours_jours).one_or_none())==False:
            print("existe pas dans DB ")
            Cour.query.filter_by(Cours_id=id).update(dict(Cours_nom=newcour.Cours_nom,Cours_jours=newcour.Cours_jours,Cours_temps=newcour.Cours_temps))
            bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('Cours/update.html',listcol=listcol, form=form, id=id)

@coursview_blueprint.route('/studentbycour.pdf',methods= ['GET','POST'])
def studentbycours_pdf():
    id = request.form['id']
    today = date.today()
    todayyear = int(today.strftime('%Y'))
    cour = Cour.query.filter_by(Cours_id=id).first()
    eleves = bd.session.query(Eleve).join(Courseleve).filter(Courseleve.Cours_Coursid == id).filter(Courseleve.year==todayyear).filter(Eleve.eleve_actif == 1).all()
    html=render_template('Cours/fichepresence.html', eleves=eleves, cour=cour)
    pdf=pdfkit.from_string(html,False,options = wkhtmltopdf_options)
    reponse=make_response(pdf)
    reponse.headers['Content-Type']='application/pdf'
    reponse.headers['Content-Disposition']="inline ; filename=coursprésence.pdf"
    return reponse

@coursview_blueprint.route('/out',methods= ['GET','POST'])
def outcour():
    id=request.form['id']
    cour= Cour.query.filter_by(Cours_id=id).first()
    cour.Cours_actif='0'
    bd.session.commit()
    return courview()

@coursview_blueprint.route('/in',methods= ['GET','POST'])
def incour():
    id=request.form['id']
    cour= Cour.query.filter_by(Cours_id=id).first()
    cour.Cours_actif=1
    bd.session.commit()
    return courview()