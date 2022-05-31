from __init__ import bd


class Professeur(bd.Model):
    prof_id = bd.Column(bd.Integer, primary_key=True)
    prof_nom = bd.Column(bd.String(45), nullable=False)
    prof_prenom = bd.Column(bd.String(45), nullable=False)
    prof_numcontact = bd.Column(bd.String(45))
    prof_mail = bd.Column(bd.String(45))
    prof_nom_prenom = bd.Column(bd.String(80))
    prof_datenaissance = bd.Column(bd.Date)
    prof_test = bd.Column(bd.Enum('1', '2'))
    cours = bd.relationship("CoursProf", back_populates="professeur")






