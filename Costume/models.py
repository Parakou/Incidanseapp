from __init__ import bd


class Costume(bd.Model):


    costume_id = bd.Column(bd.Integer, primary_key=True)
    costume_nom = bd.Column(bd.String(50), nullable=False)
    costume_description = bd.Column(bd.Text(100))
    costume_malle = bd.Column(bd.Integer,nullable=False)
    costume_quantite=bd.Column(bd.Integer, nullable=False)
    costume_taille=bd.Column(bd.String(20), nullable=False)
    costume_images=bd.Column(bd.Text(500),info={'label': 'Image'})
    costume_categorie_id=bd.Column(bd.Integer, bd.ForeignKey('categorie.categorie_id'),nullable=False)
    Categorie = bd.relationship('Categorie')
    reservation=bd.relationship("Rescost",back_populates='costume')


class Categorie(bd.Model):
    categorie_id = bd.Column(bd.Integer, primary_key=True)
    categorie_nom= bd.Column(bd.String(50), nullable=False)
    costumes = bd.relationship('Costume', backref='categorie', lazy=True)

def Listecategorie():
    return Categorie.query


class Rescost(bd.Model):
    rescost_id=bd.Column(bd.Integer, primary_key=True)
    reservation_id=bd.Column(bd.ForeignKey('reservation.reservation_id'), nullable=False, index=True)
    costume_id=bd.Column(bd.ForeignKey('costume.costume_id'), nullable=False, index=True)
    rescost_quantité=bd.Column(bd.Integer, nullable=False)
    costume=bd.relationship("Costume",back_populates="reservation")
    reservation=bd.relationship("Reservation",back_populates="costume")




class Reservation(bd.Model):

    reservation_id = bd.Column(bd.Integer, primary_key=True)
    reservation_numéro = bd.Column(bd.Integer,autoincrement=True)
    reservation_début=bd.Column(bd.Date,nullable=False,info={'label': 'Date de début de réservation'})
    reservation_fin = bd.Column(bd.Date, nullable=False, info={'label': 'Date de fin de réservation'})
    reservation_description = bd.Column(bd.Text(100),nullable=False, info={'label': 'Description de l''évenement'})
    reservation_nom=bd.Column(bd.String(50), nullable=False,info={'label': 'Nom de la réservation'})
    reservation_adressemail=bd.Column(bd.String(50), nullable=False,info={'label': 'Adresse mail de contact'})
    reservation_numtel=bd.Column(bd.String(50), nullable=False,info={'label': 'Numéro de téléphone de contact'})
    reservation_statut=bd.Column(bd.Enum('en attente', 'accepté', 'refusé'),nullable=False,server_default=bd.text("'en attente'"))
    costume=bd.relationship("Rescost",back_populates="reservation")





