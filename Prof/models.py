from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from __init__ import bd
from ville.models import Ville,Province




class Prof(bd.Model):
    __tablename__ = 'Prof'

    Prof_id = Column(Integer, primary_key=True)
    Prof_nom = Column(String(45), nullable=False)
    Prof_prenom = Column(String(45), nullable=False)
    Prof_numcontact = Column(String(45))
    Prof_mail = Column(String(45))
    Prof_nom_prenom = Column(String(80))
    Prof_datenaissance = Column(Date)
    Prof_test = Column(Enum('1', '2'))
