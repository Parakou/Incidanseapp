
from flask import render_template, flash, abort
from flask_security import auth_required, Security, LoginForm, roles_accepted
from flask_security.utils import hash_password

from Auth.models import User, Role
from Security.Auth import ExtendedLoginForm
from __init__ import create_app, bd, nav, SQLAlchemyUserDatastore,session,login_required

app=create_app()
user_datastore = SQLAlchemyUserDatastore(bd, User, Role)
security = Security(app, user_datastore,login_form=ExtendedLoginForm)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Student', 'studentview_blueprint.studentview'),

])

if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
    #bd.drop_all()
    #bd.create_all()
    if "cart" not in session:
        session["cart"]=[]
    #for d in session['cart']:
     #   print(d)
      #  if int(d.get('id'))==int(7):
       #     session['cart'].remove(d)
    print(LoginForm)
    return render_template("index.html")

@app.route('/admin')
@login_required
@roles_accepted('Admin', 'Professeur')
def admin():
    return render_template("Admin.html")







