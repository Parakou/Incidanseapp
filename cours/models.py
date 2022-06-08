from wtforms import ValidationError

from __init__ import bd

def validate_Cours_nom(form,field):
    if not bool(Cour.query.filter_by(Cours_nom=field.data).one_or_none()) == False:
        raise ValidationError("Le cour  existe deja")

class Cour(bd.Model):


    Cours_id = bd.Column(bd.Integer, primary_key=True)
    Cours_nom = bd.Column(bd.String(100), nullable=False,info={'label': 'Nom du cour','validators': [validate_Cours_nom]})
    Cours_temps = bd.Column(bd.String(10), nullable=False,info={'label': 'Durée du cour'})
    Cours_jours = bd.Column(bd.Enum('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),info={'label': 'Jour du cour'})
    Cours_actif = bd.Column(bd.Enum('1', '0'), server_default=bd.text("'1'"))
    eleve=bd.relationship("Courseleve",back_populates="cour")
    professeur=bd.relationship('CoursProf',back_populates='cour')


class Courseleve(bd.Model):


    eleve_Coursid = bd.Column(bd.Integer, primary_key=True)
    eleve_eleve_id = bd.Column(bd.ForeignKey('eleve.eleve_id'), nullable=False, index=True)
    Cours_Coursid = bd.Column(bd.ForeignKey('cour.Cours_id'), nullable=False, index=True)

    cour=bd.relationship("Cour",back_populates="eleve")
    eleve=bd.relationship("Eleve",back_populates="cours")
    year = bd.Column(bd.Integer,nullable=False)


class CoursProf(bd.Model):
    CoursProf_id = bd.Column(bd.Integer, primary_key=True)
    prof_id = bd.Column(bd.ForeignKey('professeur.prof_id'), nullable=False, index=True)
    cours_id = bd.Column(bd.ForeignKey('cour.Cours_id'), nullable=False, index=True)

    cour = bd.relationship('Cour', back_populates='professeur')
    professeur = bd.relationship('Professeur', back_populates='cours')
    year = bd.Column(bd.Integer, nullable=False)

def ListeCour():
    return Cour.query