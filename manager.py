
from flask import render_template
from flask_login import login_required
from flask_security import auth_required, Security
from flask_security.utils import hash_password

from Auth.models import User, Role
from __init__ import create_app, bd, nav, SQLAlchemyUserDatastore,session

app=create_app()
user_datastore = SQLAlchemyUserDatastore(bd, User, Role)
security = Security(app, user_datastore)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Student', 'studentview_blueprint.studentview'),

])







@app.route('/')
#@login_required
def index():
    #bd.drop_all()
    #bd.create_all()
    if "cart" not in session:
        session["cart"]=[]
    #for d in session['cart']:
     #   print(d)
      #  if int(d.get('id'))==int(7):
       #     session['cart'].remove(d)


    return render_template("index.html")
    if __name__ == '__main__':
        app.run()



