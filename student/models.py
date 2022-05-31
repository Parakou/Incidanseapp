from __init__ import bd


class Eleve(bd.Model):


    eleve_id = bd.Column(bd.Integer, primary_key=True,)
    eleve_prenom = bd.Column(bd.String(45), nullable=False,info={'label': 'Prénom'})
    eleve_nom = bd.Column(bd.String(45), nullable=False,info={'label': 'Nom'})
    eleve_datenaissance = bd.Column(bd.Date,nullable=False,info={'label': 'Date de naissance'})
    eleve_age = bd.Column(bd.Integer,info={'label': 'Age'})
    eleve_adresse = bd.Column(bd.String(100),info={'label': 'Adresse'})
    eleve_GSM = bd.Column(bd.String(45),info={'label': 'Numéro de GSM'})
    eleve_fixe = bd.Column(bd.String(45),info={'label': 'Numéro de téléphone fixe'})
    eleve_mail = bd.Column(bd.String(45),info={'label': 'Adresse mail'})
    eleve_mail2 = bd.Column(bd.String(45),info={'label': 'Adresse mail 2'})
    eleve_heure = bd.Column(bd.String(45))
    eleve_freresoeur = bd.Column(bd.Enum('1', '0'), server_default=bd.text("'0'"),info={'choices':[('1', "Non"), ('1', 'Oui')],'label': 'Frère ou Soeur'})
    eleve_medic = bd.Column(bd.Text(100),info={'label': 'Remarque Médical'})
    eleve_courst = bd.Column(bd.String(45))
    eleve_actif = bd.Column(bd.Enum('1', '0'), server_default=bd.text("'1'"))
    Ville_id_Ville = bd.Column(bd.ForeignKey('ville.ville_ID'), nullable=False, index=True)
    eleve_nom_prenom = bd.Column(bd.String(100))
    cours=bd.relationship("Courseleve", back_populates="eleve")
    Ville = bd.relationship('Ville')




