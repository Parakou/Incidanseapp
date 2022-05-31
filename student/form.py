from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import QuerySelectField,QuerySelectMultipleField,widgets
from cours.models import ListeCour
from student.models import Eleve
from ville.models import ListeVille


class EleveForm(ModelForm, FlaskForm):
    class Meta:
        model = Eleve
    ville=QuerySelectField(query_factory=ListeVille, get_label=(lambda Ville: Ville.ville_nom + " " + str(Ville.ville_CP)), allow_blank=False)
    cours=QuerySelectMultipleField(query_factory=ListeCour,get_label=(lambda Cour: Cour.Cours_nom+" "+Cour.Cours_jours), allow_blank=False,widget=widgets.ListWidget(prefix_label=False),
            option_widget=widgets.CheckboxInput())

