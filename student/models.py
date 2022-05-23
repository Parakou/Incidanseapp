from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from __init__ import bd
from ville.models import Ville,Province
from cours.models import Courseleve

class Eleve(bd.Model):
    __tablename__ = 'Eleve'

    eleve_id = Column(Integer, primary_key=True)
    eleve_prenom = Column(String(45), nullable=False)
    eleve_nom = Column(String(45), nullable=False)
    eleve_datenaissance = Column(Date)
    eleve_age = Column(Integer)
    eleve_adresse = Column(String(100))
    eleve_GSM = Column(String(45))
    eleve_fixe = Column(String(45))
    eleve_mail = Column(String(45))
    eleve_mail2 = Column(String(45))
    eleve_heure = Column(String(45))
    eleve_freresoeur = Column(Enum('1', '0'), server_default=text("'0'"))
    eleve_medic = Column(String(100))
    eleve_courst = Column(String(45))
    eleve_actif = Column(Enum('1', '0'), server_default=text("'1'"))
    Ville_id_Ville = Column(ForeignKey('Ville.Ville_ID'), nullable=False, index=True)
    eleve_nom_prenom = Column(String(100))

    Ville = relationship('Ville')