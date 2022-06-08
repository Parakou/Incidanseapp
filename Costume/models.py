import datetime

from wtforms import ValidationError
from wtforms.validators import email

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
    costume_actif = bd.Column(bd.Enum('1', '0'), server_default=bd.text("'1'"))

def validate_categorie_nom(form,field):
    if not bool(Categorie.query.filter_by(categorie_nom=field.data).one_or_none()) == False:
        raise ValidationError("Catégorie existe deja")

class Categorie(bd.Model):
    categorie_id = bd.Column(bd.Integer, primary_key=True)
    categorie_nom= bd.Column(bd.String(50), nullable=False,info={'label': 'Nom catégorie','validators': [validate_categorie_nom]})
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

def validate_reservation_fin(form, field):
    if field.data < form.reservation_début.data:
        raise ValidationError("La date de fin doit être postérieure à la date de début")

def validate_reservation_début(form,field):
    if field.data < datetime.date.today():
        raise ValidationError("La date de début doit être supérieur à la date du jour")

def validate_reservation_description(form,field):
    if str.isspace(form.reservation_description.data):
        raise ValidationError("Veuillez compléter une brève description de l'événement")



class Reservation(bd.Model):

    reservation_id = bd.Column(bd.Integer, primary_key=True)
    reservation_début=bd.Column(bd.Date,nullable=False,info={'label': 'Date de début de réservation','validators': [validate_reservation_début]})
    reservation_fin = bd.Column(bd.Date, nullable=False, info={'label': 'Date de fin de réservation','validators': [validate_reservation_fin]})
    reservation_description = bd.Column(bd.Text(100),nullable=False, info={'label': 'Description de l''évenement'})
    reservation_nom=bd.Column(bd.String(50), nullable=False,info={'label': 'Nom de la réservation'})
    reservation_adressemail=bd.Column(bd.String(50), nullable=False,info={'label': 'Adresse mail de contact','validators': [email()]})
    reservation_numtel=bd.Column(bd.String(50), nullable=False,info={'label': 'Numéro de téléphone de contact','validators': [validate_reservation_description]})
    reservation_statut=bd.Column(bd.Enum('en attente', 'accepté', 'refusé'),nullable=False,server_default=bd.text("'en attente'"))
    costume=bd.relationship("Rescost",back_populates="reservation")



