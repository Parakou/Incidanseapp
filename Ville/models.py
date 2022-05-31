from flask import Blueprint
from __init__ import bd

studentview_blueprint = Blueprint('models_blueprint', __name__)

class Ville(bd.Model):

    ville_ID = bd.Column(bd.Integer, primary_key=True)
    ville_nom = bd.Column(bd.String(45, 'utf8mb4_unicode_520_ci'))
    ville_CP = bd.Column(bd.Integer)
    province_id = bd.Column(bd.ForeignKey('province.province_id'), nullable=False, index=True)
    province = bd.relationship('Province')



class Province(bd.Model):


    province_id = bd.Column(bd.Integer, primary_key=True)
    province_nom = bd.Column(bd.String(45))


def ListeVille():
    return Ville.query
