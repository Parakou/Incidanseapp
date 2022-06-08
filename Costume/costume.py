import json
import os
import random
import string

from sqlalchemy import func


from __init__ import db,bd,session
from flask import render_template, request, Blueprint, jsonify

from Costume.models import Costume, Reservation, Categorie, Rescost
from Costume.form import CostumeForm, ReservationForm

costume_blueprint = Blueprint('costume_blueprint', __name__)



@costume_blueprint.route('/',methods= ['GET','POST'])
def costumeview():
        """"
        costumes=Costume.query.all()

        for costume in costumes:
            costume.costume_images= costume.costume_images.strip('][').split(';!')
        """
        costumes = bd.session.query(Costume.costume_nom, Costume.costume_images,
                                    func.group_concat(Costume.costume_taille).label("costume_taille")).group_by(
                Costume.costume_nom, Costume.costume_images)
        return render_template('Costume/costume.html',costumes=costumes)

@costume_blueprint.route('/add',methods= ['GET','POST'])
def costumeadd():
    form=CostumeForm()
    tagrandom=get_random_string(40)
    listcol=Costume.metadata.tables['costume'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('costume_id','costume_images','reservation','costume_images','costume_categorie_id')]
    listcol.extend(['Categorie'])
    if form.validate_on_submit():
        tag = request.form['tag']
        newcost=Costume()
        for attr in listcol:
            if attr !="costume_taille" and attr != "costume_quantite":
                setattr(newcost, attr, form[attr].data)
        newcost.costume_categorie_id=form.Categorie.data.categorie_id
        if bool(Costume.query.filter_by(costume_nom=newcost.costume_nom).one_or_none())==False:
            print("existe pas dans DB ")
            costumefolder="static/Costumeimage/"
            folder = os.listdir(costumefolder+"upload")
            num = 1
            if not os.path.exists("static/Costumeimage/"+newcost.costume_nom):
                os.makedirs("static/Costumeimage/"+newcost.costume_nom)
            for index, file in enumerate(folder):
                if file.startswith(tag):
                    os.rename(costumefolder+"upload/" + file,costumefolder+newcost.costume_nom+"/"+newcost.costume_nom + "_" + str(num) + ".jpg")
                    num = num + 1
            pathimage=""
            listfoldercostume=os.listdir(costumefolder+newcost.costume_nom)
            num=num-1
            for image in listfoldercostume:
                if image==(newcost.costume_nom + "_" + str(num) + ".jpg"):
                    var=costumefolder+newcost.costume_nom+"/"+image
                else:
                    var = costumefolder + newcost.costume_nom + "/" + image+";!"
                pathimage+=var
            newcost.costume_images=pathimage
            for taille,quantite in zip(form["costume_taille"].data,form["costume_quantite"].data):
                newcost1=Costume()
                newcost1.costume_nom=newcost.costume_nom
                newcost1.costume_images=newcost.costume_images
                newcost1.costume_categorie_id=newcost.costume_categorie_id
                newcost1.costume_description=newcost.costume_description
                newcost1.costume_malle=newcost.costume_malle
                newcost1.costume_taille=taille
                newcost1.costume_quantite=quantite
                bd.session.add(newcost1)
                bd.session.commit()
        else:
           print("Existe dans db")
        return render_template('index.html')
    return render_template('Costume/add.html', listcol=listcol, form=form, num=tagrandom)

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str

@costume_blueprint.route('/upload', methods= ['GET','POST'])
def handle_upload():
    print("lancé")
    for key, f in request.files.items():
        print("coucou")
        print(key)
        f.filename=key+".jpg"
        print(f.filename)
        f.save(os.path.join("static/Costumeimage/upload", f.filename))
    return '', 204

"""
-------------------------------------------------
"""
""""
@costume_blueprint.route('/reservation',methods= ['GET','POST'])
def addreservation():
    form = ReservationForm()
    listcol = Reservation.metadata.tables['reservation'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('reservation_id','reservation_statut',)]
    listcol.extend([ 'cours'])
    today = date.today()
    if form.validate_on_submit():
        newprof = Reservation()
        for attr in listcol:
            if attr != "cours":
                setattr(newprof, attr, form[attr].data)
            print("existe pas dans DB ")
            for cour in form.cours.data:
                newCoursProf = Reservation()
                newCoursProf.cour = cour
                newCoursProf.year = int(today.strftime('%Y'))
                newprof.cours.append(newCoursProf)
            bd.session.commit()
        else:
            print("Existe dans db")
        return render_template('index.html')
    return render_template('Prof/add.html', listcol=listcol, form=form)
"""

@costume_blueprint.route('/calendrier', methods= ['GET','POST'])
def calendrier():
    return render_template('Costume/calendrier.html')

@costume_blueprint.route('/product/<id>', methods= ['GET','POST'])
def product(id):
    costume=bd.session.query(Costume.costume_nom, Costume.costume_images,func.group_concat(Costume.costume_taille).label("costume_taille"),Categorie.categorie_nom,Costume.costume_description).join(Categorie,Costume.costume_categorie_id==Categorie.categorie_id).filter(Costume.costume_nom == id).group_by(Costume.costume_nom, Costume.costume_images,Categorie.categorie_nom,Costume.costume_description)
    images=[]
    for image in costume:
        images=image.costume_images.split(';!')
    options=Costume.query.filter_by(costume_nom=id).all()
    categorie=options[0].costume_categorie_id
    catcostumes=bd.session.query(Costume.costume_nom, Costume.costume_images,func.group_concat(Costume.costume_taille).label("costume_taille")).filter(Costume.costume_categorie_id == categorie).filter(Costume.costume_nom != id).group_by(Costume.costume_nom, Costume.costume_images).order_by(func.rand()).limit(4)
    producart = 0
    if 'cart' in session:
        for d in session['cart']:
            producart=producart+int(d.get('qt'))

    cart=session['cart']
    return render_template('Costume/Fiche costume.html',costumes=costume,images=images,options=options,catcostumes=catcostumes,productcart=producart,cart=cart)

@costume_blueprint.route('/additemcart', methods= ['GET','POST'])
def additem():
    # This is the product being viewed on the page.
    costume = Costume.query.get(request.form.get('id'))
    preview= costume.costume_images.split(';!')
    preview=preview[0]
    print(preview)
    if 'cart' in session:
            # If the product is not in the cart, then add it.
        if not any(costume.costume_nom in d for d in session['cart']):
                session['cart'].append({"id":request.form.get('id'),"Nomcostume":costume.costume_nom,"Taille": request.form.get('size'),"qt":request.form.get("qt"),"preview":preview})
            # If the product is already in the cart, update the quantity
        elif any(costume.costume_nom  in d for d in session['cart']):
            for d in session['cart']:
                d.update((k, request.form.get('size')) for k, v in d.items() if k == costume.costume_nom)
    else:
            # In this block, the user has not started a cart, so we start it for them and add the product.
        session['cart'] = [{costume.costume_nom:request.form.get('size')}]

    return jsonify(session['cart'])


@costume_blueprint.route('/removeitemcart', methods= ['GET','POST'])
def removeitem():
    # This is the product being viewed on the page.
    print(request.form.get('id'))
    costume = Costume.query.get(request.form.get('id'))
    if 'cart' in session:
     for d in session['cart']:
      if int(d.get('id'))==int(request.form.get('id')):
        session['cart'].remove(d)
    return ('', 204)

@costume_blueprint.route('/cal', methods= ['GET','POST'])
def callcal():
    reservationencours=Costume.query.filter_by(costume_id=int(request.form.get('data'))).first()
    events = []
    for a in reservationencours.reservation:
        if a.reservation.reservation_statut=="accepté":
            events.append({
                            'end':a.reservation.reservation_fin.strftime('20%y-%m-%d'),
                            'start':a.reservation.reservation_début.strftime('20%y-%m-%d'),
                            'title':reservationencours.costume_nom+""+reservationencours.costume_taille},)
    return jsonify(events)

@costume_blueprint.route('/testeur', methods= ['GET','POST'])
def testeur():
    cart = session["cart"]
    print(len(session["cart"]))
    return render_template('Costume/calendrier.html', cart=cart)

@costume_blueprint.route('/reservation', methods= ['GET','POST'])
def reservation():
    cart = session["cart"]
    costumes=[]
    form = ReservationForm()
    listcol = Costume.metadata.tables['reservation'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('reservation_id', 'reservation_statut', 'reservation', 'reservation_numéro','reservation_description')]
    for id in cart:
        costumes.append(Costume.query.get(id.get('id')))
    print('Yo')
    if request.form.get("submitbutton")=="reservsubmit":
        print('Valide')
        newreserv=Reservation()
        for attr in listcol:
                setattr(newreserv, attr, form[attr].data)
        newreserv.reservation_description=form["reservation_description"].data
        newreserv.reservation_statut="en attente"
        for costume in session["cart"]:
            costumeq = Costume.query.filter_by(costume_id=costume.get('id')).first()
            print(type(costume.get('id')))
            print(type(costumeq.costume_id))
            print(costume)
            if int(costume.get('id'))==costumeq.costume_id:
                print("go")
                print(costumeq.costume_id)
                print(costume.get('qt'))
                newresvcost=Rescost()
                newresvcost.rescost_quantité=int(costume.get('qt'))
                newresvcost.costume=costumeq
                newreserv.costume.append(newresvcost)
            else:
                print("ben merde")
        print(newreserv)
        bd.session.add(newreserv)
        bd.session.commit()
        session["cart"]=[]
        return render_template('index.html')
    return render_template('Costume/reservation.html', listcol=listcol,cart=cart, costumes=costumes,form=form)
