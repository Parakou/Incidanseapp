from __init__ import bd


class Professeur(bd.Model):
    prof_id = bd.Column(bd.Integer, primary_key=True)
    prof_nom = bd.Column(bd.String(45), nullable=False,info={'label': 'Nom du professeur'})
    prof_prenom = bd.Column(bd.String(45), nullable=False,info={'label': 'Prénom du professeur'})
    prof_numcontact = bd.Column(bd.String(45),info={'label': 'Numéro de contact'})
    prof_mail = bd.Column(bd.String(45),info={'label': 'Adresse mail'})
    prof_datenaissance = bd.Column(bd.Date,info={'label': 'Date de naissance'})
    prof_actif = bd.Column(bd.Enum('1', '0'), server_default=bd.text("'1'"))
    cours = bd.relationship("CoursProf", back_populates="professeur")
