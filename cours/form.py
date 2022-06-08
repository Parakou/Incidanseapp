from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from cours.models import Cour


class Courform(ModelForm,FlaskForm):
    class Meta:
        model = Cour
        exclude = ['Cours_actif']
