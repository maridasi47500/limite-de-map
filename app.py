from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,phone,country_id) values (:username,:email,:password,:phone,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into city (country_id,name) values (:country_id,:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from city')


        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)

@app.route("/add_one_uservisitcountry", methods=["GET","POST"])
def add_one_uservisitcountry():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['photo']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["photo"]=uploaded_file.filename


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into uservisitcountry (user_id,country_id,decouverte_coin_monde,photo) values (:user_id,:country_id,:decouverte_coin_monde,:photo)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from uservisitcountry')


        return render_template("uservisitcountryform.html", uservisitcountrys=user, one_user=one_user, the_title="add new uservisitcountry", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from uservisitcountry')
    one_user = query_db("select * from uservisitcountry limit 1", one=True)
    return render_template("uservisitcountryform.html", uservisitcountrys=user, one_user=one_user, the_title="add new uservisitcountry", touslescountry=touslescountry)

@app.route("/add_one_debutlimitmap", methods=["GET","POST"])
def add_one_debutlimitmap():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into debutlimitmap (lat,lon) values (:lat,:lon)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from debutlimitmap')


        return render_template("debutlimitmapform.html", debutlimitmaps=user, one_user=one_user, the_title="add new debutlimitmap")


    user = query_db('select * from debutlimitmap')
    one_user = query_db("select * from debutlimitmap limit 1", one=True)
    return render_template("debutlimitmapform.html", debutlimitmaps=user, one_user=one_user, the_title="add new debutlimitmap")



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
@app.route("/add_one_finlimitdemap", methods=["GET","POST"])
def add_one_finlimitdemap():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into finlimitdemap (lat,lon) values (:lat,:lon)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from finlimitdemap')


        return render_template("finlimitdemapform.html", finlimitdemaps=user, one_user=one_user, the_title="add new finlimitdemap")


    user = query_db('select * from finlimitdemap')
    one_user = query_db("select * from finlimitdemap limit 1", one=True)
    return render_template("finlimitdemapform.html", finlimitdemaps=user, one_user=one_user, the_title="add new finlimitdemap")



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
@app.route("/add_one_boundingbox", methods=["GET","POST"])
def add_one_boundingbox():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into boundingbox (debutlimitmap_id,finlimitdemap_id,user_id) values (:debutlimitmap_id,:finlimitdemap_id,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from boundingbox')


        return render_template("boundingboxform.html", boundingboxs=user, one_user=one_user, the_title="add new boundingbox", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from boundingbox')
    one_user = query_db("select * from boundingbox limit 1", one=True)
    return render_template("boundingboxform.html", boundingboxs=user, one_user=one_user, the_title="add new boundingbox", touslesuser=touslesuser)

@app.route("/add_one_limitdemaphasmusic", methods=["GET","POST"])
def add_one_limitdemaphasmusic():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into limitdemaphasmusic (boundingbox_id,artist,title) values (:boundingbox_id,:artist,:title)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from limitdemaphasmusic')


        return render_template("limitdemaphasmusicform.html", limitdemaphasmusics=user, one_user=one_user, the_title="add new limitdemaphasmusic")


    user = query_db('select * from limitdemaphasmusic')
    one_user = query_db("select * from limitdemaphasmusic limit 1", one=True)
    return render_template("limitdemaphasmusicform.html", limitdemaphasmusics=user, one_user=one_user, the_title="add new limitdemaphasmusic")

@app.route("/add_one_boundingboxhaslimitsound", methods=["GET","POST"])
def add_one_boundingboxhaslimitsound():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into boundingboxhaslimitsound (boundingboxid,sound,souvenir_description) values (:boundingboxid,:sound,:souvenir_description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from boundingboxhaslimitsound')


        return render_template("boundingboxhaslimitsoundform.html", boundingboxhaslimitsounds=user, one_user=one_user, the_title="add new boundingboxhaslimitsound")


    user = query_db('select * from boundingboxhaslimitsound')
    one_user = query_db("select * from boundingboxhaslimitsound limit 1", one=True)
    return render_template("boundingboxhaslimitsoundform.html", boundingboxhaslimitsounds=user, one_user=one_user, the_title="add new boundingboxhaslimitsound")

@app.route("/add_one_boudingboxhassouvenir", methods=["GET","POST"])
def add_one_boudingboxhassouvenir():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['video']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["video"]=uploaded_file.filename


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into boudingboxhassouvenir (video,user_id,boundingbox_id,description) values (:video,:user_id,:boundingbox_id,:description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from boudingboxhassouvenir')


        return render_template("boudingboxhassouvenirform.html", boudingboxhassouvenirs=user, one_user=one_user, the_title="add new boudingboxhassouvenir", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from boudingboxhassouvenir')
    one_user = query_db("select * from boudingboxhassouvenir limit 1", one=True)
    return render_template("boudingboxhassouvenirform.html", boudingboxhassouvenirs=user, one_user=one_user, the_title="add new boudingboxhassouvenir", touslesuser=touslesuser)

