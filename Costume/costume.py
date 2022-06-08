import json
import os
import random
import string

import kwargs as kwargs
from sqlalchemy import func


from __init__ import bd,session
from flask import render_template, request, Blueprint, jsonify, flash, abort

from Costume.models import Costume, Reservation, Categorie, Rescost
from Costume.form import CostumeForm, ReservationForm, CategorieForm

costume_blueprint = Blueprint('costume_blueprint', __name__)



@costume_blueprint.route('/',methods= ['GET','POST'])
def costumeview():
        """"
        costumes=Costume.query.all()

        for costume in costumes:
            costume.costume_images= costume.costume_images.strip('][').split(';!')
        """
        costumes = bd.session.query(Costume.costume_nom, Costume.costume_images,func.group_concat(Costume.costume_taille).label("costume_taille")).group_by(Costume.costume_nom, Costume.costume_images).filter(Costume.costume_actif== 1)
        return render_template('Costume/costume.html',costumes=costumes)

@costume_blueprint.route('/listecostume',methods= ['GET','POST'])
def listecostume():
    costumes =Costume.query.filter_by(costume_actif=1).all()
    marqueur="actuel"
    return render_template('Costume/listedescostumes.html',costumes=costumes,marqueur=marqueur)

@costume_blueprint.route('/out',methods= ['GET','POST'])
def outcostume():
    id=request.form['id']
    print(id)
    costume= Costume.query.filter_by(costume_id=id).first()
    print(costume.costume_nom)
    costume.costume_actif="0"
    bd.session.commit()
    return listecostume()

@costume_blueprint.route('/in',methods= ['GET','POST'])
def incostume():
    id=request.form['id']
    costume = Costume.query.filter_by(costume_id=id).first()
    print(costume.costume_nom)
    costume.costume_actif="1"
    print(costume.costume_actif)
    bd.session.commit()
    return listecostume()

@costume_blueprint.route('/anciencour',methods= ['GET','POST'])
def costumeold():
    costumes=Costume.query.filter_by(costume_actif="0").all()
    marqueur="old"
    return render_template('Costume/listedescostumes.html', costumes=costumes,marqueur=marqueur)

@costume_blueprint.route('/add',methods= ['GET','POST'])
def costumeadd():
    form=CostumeForm()
    tagrandom=get_random_string(40)
    listcol=Costume.metadata.tables['costume'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('costume_id','costume_images','reservation','costume_images','costume_categorie_id',"costume_actif")]
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

@costume_blueprint.route('/<id>', methods= ['GET','POST'])
def product(id):
    costume=bd.session.query(Costume.costume_nom, Costume.costume_images,func.group_concat(Costume.costume_taille).label("costume_taille"),Categorie.categorie_nom,Costume.costume_description).join(Categorie,Costume.costume_categorie_id==Categorie.categorie_id).filter(Costume.costume_nom == id).group_by(Costume.costume_nom, Costume.costume_images,Categorie.categorie_nom,Costume.costume_description)
    images=[]
    print(costume)
    for image in costume:
        images=image.costume_images.split(';!')
    options=Costume.query.filter_by(costume_nom=id,costume_actif="1").all()
    options2=Costume.query.filter_by(costume_nom=id).all()
    print(options2)
    if not options:
        if not options2:
            abort(404)
        else:
            abort(410)
    categorie=options[0].costume_categorie_id
    catcostumes=bd.session.query(Costume.costume_nom, Costume.costume_images,func.group_concat(Costume.costume_taille).label("costume_taille")).filter(Costume.costume_categorie_id == categorie).filter(Costume.costume_nom != id).group_by(Costume.costume_nom, Costume.costume_images).filter(Costume.costume_actif== 1).order_by(func.rand()).limit(4)
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
    if  session['cart']:
        print("1")
        for a in session['cart']:
            print(a["id"])
            if a["id"]==costume.costume_id:
                print("2")
                a["qt"]=request.form.get("qt")
                return jsonify(session['cart'])
        print("3")
        session['cart'].append({"id":costume.costume_id,"Nomcostume":costume.costume_nom,"Taille": costume.costume_taille,"qt":request.form.get("qt"),"preview":preview})
        return jsonify(session['cart'])

    else:
        # In this block, the user has not started a cart, so we start it for them and add the product.
        print("11")
        session['cart'] = [{"id":costume.costume_id,"Nomcostume":costume.costume_nom,"Taille": costume.costume_taille,"qt":request.form.get("qt"),"preview":preview}]



    """
        if not any(costume.costume_id in a for d, a in session['cart']):
            print("option 1")
            session['cart'].append({"id":costume.costume_id,"Nomcostume":costume.costume_nom,"Taille": costume.costume_taille,"qt":request.form.get("qt"),"preview":preview})
            # If the product is already in the cart, update the quantity
        elif any(costume.costume_nom  in a for d,a in session['cart']):
            print("option 2")
            for d in session['cart']:
                d.update((k, request.form.get('size')) for k, v in d.items() if k == costume.costume_id)
    else:
            # In this block, the user has not started a cart, so we start it for them and add the product.
        session['cart'] = [{costume.costume_nom:request.form.get('size')}]
    """
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


@costume_blueprint.route('/updatecostume',methods= ['GET','POST'])
def costumeupdte():
    id = request.form['id']
    print(id)
    costume = Costume.query.get(request.form.get('id'))
    tagrandom = get_random_string(40)
    costume2=Costume(costume_id=costume.costume_id,costume_nom=costume.costume_nom)
    form = CostumeForm(obj=costume2)
    print('rs')
    listcol = Costume.metadata.tables['costume'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('costume_id','costume_images','reservation','costume_images','costume_categorie_id',"costume_actif")]
    if form.validate_on_submit():
        tag = request.form['tag']
        newcost = Costume()
        for attr in listcol:
            if attr != "costume_taille" and attr != "costume_quantite":
                setattr(newcost, attr, form[attr].data)
        newcost.costume_categorie_id = form.Categorie.data.categorie_id
        if bool(Costume.query.filter_by(costume_nom=newcost.costume_nom).one_or_none()) == False:
            print("existe pas dans DB ")
            costumefolder = "static/Costumeimage/"
            folder = os.listdir(costumefolder + "upload")
            num = 1
            if not os.path.exists("static/Costumeimage/" + newcost.costume_nom):
                os.makedirs("static/Costumeimage/" + newcost.costume_nom)
            for index, file in enumerate(folder):
                if file.startswith(tag):
                    os.rename(costumefolder + "upload/" + file,
                              costumefolder + newcost.costume_nom + "/" + newcost.costume_nom + "_" + str(num) + ".jpg")
                    num = num + 1
            pathimage = ""
            listfoldercostume = os.listdir(costumefolder + newcost.costume_nom)
            num = num - 1
            for image in listfoldercostume:
                if image == (newcost.costume_nom + "_" + str(num) + ".jpg"):
                    var = costumefolder + newcost.costume_nom + "/" + image
                else:
                    var = costumefolder + newcost.costume_nom + "/" + image + ";!"
                pathimage += var
            newcost.costume_images = pathimage
            for taille, quantite in zip(form["costume_taille"].data, form["costume_quantite"].data):
                newcost1 = Costume()
                newcost1.costume_nom = newcost.costume_nom
                newcost1.costume_images = newcost.costume_images
                newcost1.costume_categorie_id = newcost.costume_categorie_id
                newcost1.costume_description = newcost.costume_description
                newcost1.costume_malle = newcost.costume_malle
                newcost1.costume_taille = taille
                newcost1.costume_quantite = quantite
                bd.session.add(newcost1)
                bd.session.commit()
        else:
            print("Existe dans db")
        return render_template('index.html')
    return render_template('Costume/add.html', listcol=listcol, form=form, num=tagrandom)


@costume_blueprint.route('/<id>/details',methods= ['GET','POST'])
def costumedetails(id):
    costume = Costume.query.filter_by(costume_id=id).first()
    for i in costume.reservation:
        print(i.reservation.reservation_début)
        print(i.reservation.reservation_fin)

    return render_template('Costume/costumedetails.html',costume=costume)

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


@costume_blueprint.route('/reservation', methods= ['GET','POST'])
def reservation():
    cart = session["cart"]
    costumes=[]
    form = ReservationForm()
    listcol = Costume.metadata.tables['reservation'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('reservation_id', 'reservation_statut', 'reservation','reservation_description')]
    for id in cart:
        costumes.append(Costume.query.get(id.get('id')))
    print('Yo')
    if request.form.get("submitbutton")=="reservsubmit":
        print('Valide')
        newreserv = Reservation()
        if form.validate_on_submit():
            print("validée")
            print(len(form.reservation_description.data))
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
        else:
                for c in form.errors:
                    print(c)
                    for a in form.reservation_description.errors:
                        print(a)
                if form.reservation_description.errors:
                    print("yooo")
                else:
                    print("nope")
    return render_template('Costume/reservation.html', listcol=listcol,cart=cart, costumes=costumes,form=form)

@costume_blueprint.route('/reservationliste', methods= ['GET','POST'])
def reservationliste():
    listereservation=Reservation.query.filter_by(reservation_statut='en attente').all()
    print(listereservation)
    return  render_template('Costume/resarvationliste.html',listereservation=listereservation)

@costume_blueprint.route('/reservation/<id>',methods= ['GET','POST'])
def ficherreservation(id):
    reservationliste = Reservation.query.filter_by(reservation_id=id).first()
    return render_template('Costume/reservationfiche.html',reservation=reservationliste)

@costume_blueprint.route('/categorie',methods= ['GET','POST'])
def catadd():
    form=CategorieForm()
    listcol=Costume.metadata.tables['categorie'].columns.keys()
    listcol = [attribut for attribut in listcol if attribut not in ('categorie_id')]
    if request.form.get("submitbutton") == "catsubmit":
        print("tes")
        if form.validate_on_submit():
            newcat=Categorie()
            for attr in listcol:
                setattr(newcat, attr, form[attr].data.capitalize())
            print("existe pas dans DB ")
            bd.session.add(newcat)
            bd.session.commit()
            return render_template('index.html')
        else:
           print("Existe dans db")
           return render_template('Costume/addcat.html', listcol=listcol, form=form)
    else:
        print("raté")
        return render_template('Costume/addcat.html', listcol=listcol, form=form)

@costume_blueprint.route('/acceptation', methods= ['GET','POST'])
def reservationac():
    id = request.form['id']
    reservation = Reservation.query.filter_by(reservation_id=id).first()
    reservation.reservation_statut="accepté"
    bd.session.commit()
    return  reservationliste()

@costume_blueprint.route('/refuser', methods= ['GET','POST'])
def reservationden():
    id = request.form['id']
    reservation = Reservation.query.filter_by(reservation_id=id).first()
    reservation.reservation_statut="refusé"
    bd.session.commit()
    return  reservationliste()

@costume_blueprint.route('/reservationlister', methods= ['GET','POST'])
def reservationlisterefuse():
    listereservation=Reservation.query.filter_by(reservation_statut='refusé').all()
    print(listereservation)
    return  render_template('Costume/resarvationliste.html',listereservation=listereservation)

@costume_blueprint.route('/reservationlistera', methods= ['GET','POST'])
def reservationlisteacc():
    listereservation=Reservation.query.filter_by(reservation_statut='accepté').all()
    print(listereservation)
    return  render_template('Costume/resarvationliste.html',listereservation=listereservation)
"""
<----------------->
"""
@costume_blueprint.errorhandler(410)
def internal_server_error(error):
    return render_template('Error/Costume/510.html'), 410

@costume_blueprint.errorhandler(404)
def internal_server_error(error):
    return render_template('Error/Costume/404.html'), 404