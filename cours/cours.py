from flask import render_template, request, Blueprint, url_for, make_response
import pdfkit

from __init__ import bd
from cours.models import Cour,Courseleve
from student.models import Eleve
from cours.form import Courform

wkhtmltopdf_options = {
    #'enable-local-file-access': True,
}

coursview_blueprint = Blueprint('coursview_blueprint', __name__)


@coursview_blueprint.route('/',methods= ['GET','POST'])
def courview():
        cours=Cour.query.all()
        return render_template('Cours/cours.html', cours=cours)


@coursview_blueprint.route('/add',methods= ['GET','POST'])

def couradd():
    form=Courform()
    listcol=Cour.metadata.tables['cour'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('Cours_id')]
    if form.validate_on_submit():
        newcour=Cour()
        for attr in listcol:
            setattr(newcour, attr, form[attr].data)
        if bool(Cour.query.filter_by(Cours_nom=newcour.Cours_nom, Cours_jours=newcour.Cours_jours).one_or_none())==False:
            print("existe pas dans DB ")
            bd.session.add(newcour)
            bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('Cours/add.html',listcol=listcol, form=form)

@coursview_blueprint.route('/studentbycour',methods= ['GET','POST'])
def studentbycours():
    id=request.form['id']
    cour=Cour.query.filter_by(Cours_id=id).first()
    eleves=bd.session.query(Eleve).join(Courseleve).filter(Courseleve.Cours_Coursid==id).filter(Eleve.eleve_actif==1).all()
    return render_template('Cours/studentcour.html',eleves=eleves,cour=cour)

@coursview_blueprint.route('/update',methods= ['GET','POST'])
def courupdate():
    id = request.form['id']
    form=Courform(obj=Cour.query.filter_by(Cours_id=id).first())
    listcol=Cour.metadata.tables['cour'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('Cours_id')]
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
    cour = Cour.query.filter_by(Cours_id=id).first()
    eleves = bd.session.query(Eleve).join(Courseleve).filter(Courseleve.Cours_Coursid == id).filter(Eleve.eleve_actif == 1).all()
    html=render_template('Cours/test.html', eleves=eleves, cour=cour)

    test="Hello"
    toast="michel"
    #html = render_template('Cours/test.html', eleves=test, cour=toast)

    pdf=pdfkit.from_string(html,False,options = wkhtmltopdf_options)

    reponse=make_response(pdf)
    reponse.headers['Content-Type']='application/pdf'
    reponse.headers['Content-Disposition']="inline ; filename=coursprésence.pdf"
    return reponse
