from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from Prof.models import Professeur
from wtforms_alchemy.fields import QuerySelectMultipleField,widgets
from cours.models import ListeCour



class ProfForm(ModelForm,FlaskForm):
    class Meta:
        model = Professeur
    cours = QuerySelectMultipleField(query_factory=ListeCour,get_label=(lambda Cour: Cour.Cours_nom + " " + Cour.Cours_jours),allow_blank=False, widget=widgets.ListWidget(prefix_label=False),option_widget=widgets.CheckboxInput())