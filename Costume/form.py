from flask_wtf import FlaskForm
from wtforms import MultipleFileField, FieldList, StringField
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import QuerySelectField,QuerySelectMultipleField,widgets
from cours.models import ListeCour
from Costume.models import Costume, Reservation, Categorie, Listecategorie


class CostumeForm(ModelForm,FlaskForm):
    class Meta:
        model = Costume
    costume_taille=FieldList(StringField('costume_taille'), min_entries=1,label="Taille fringue")
    costume_quantite=FieldList(StringField('costume_quantite'), min_entries=1,label="Quantité de cette taille")
    Categorie=QuerySelectField(query_factory=Listecategorie, get_label=(lambda Categorie: Categorie.categorie_nom), allow_blank=False)


class ReservationForm(ModelForm,FlaskForm):
    class Meta:
        model = Reservation

class CategorieForm(ModelForm,FlaskForm):
    class Meta:
        model = Categorie
