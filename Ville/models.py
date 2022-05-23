from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, text
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from __init__ import bd


studentview_blueprint = Blueprint('models_blueprint', __name__)

class Ville(bd.Model):
    __tablename__ = 'Ville'
    Ville_ID = Column(Integer, primary_key=True)
    Ville_nom = Column(String(45, 'utf8mb4_unicode_520_ci'))
    Ville_CP = Column(Integer)
    Province_Province_id = Column(ForeignKey('Province.Province_id'), nullable=False, index=True)
    Province_Province = relationship('Province')



class Province(bd.Model):
    __tablename__ = 'Province'

    Province_id = Column(Integer, primary_key=True)
    Province_nom = Column(String(45))