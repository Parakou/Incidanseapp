from flask import Blueprint, render_template_string, render_template
from flask_login import login_required

from flask_security import auth_required
authblueprint = Blueprint('authblueprint', __name__)

@authblueprint.route('/home',methods= ['GET','POST'])
@login_required
def home():
    print("Yo")
    return render_template_string("Hello {{ current_user.email }}")

@authblueprint.route('/login')
def login():
    return render_template('login.html')