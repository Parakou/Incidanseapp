from flask_security import LoginForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedLoginForm(LoginForm):
    email = StringField("Nom d'utilisateur", [DataRequired()])
