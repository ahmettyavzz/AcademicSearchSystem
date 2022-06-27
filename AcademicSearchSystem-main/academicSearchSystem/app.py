from flask import Flask, config, render_template, flash, redirect, url_for, session, logging, request, render_template
from wtforms import Form, StringField, PasswordField
from functools import wraps 

import numpy as np
import random
import pandas as pd
from neo4j import GraphDatabase

#Kullanıcı giriş decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.", "danger")
            return redirect(url_for("login"))
    return decorated_function       

#Admin Giriş Formu
class LoginForm(Form): 
    email= StringField("Kullanıcı Adı:")
    password = PasswordField("Parola: ")

#Yazar Formu
class WriterForm(Form): 
    name = StringField("Adı:")
    surname = StringField("Soyadı:")
    publicationName = StringField("Yayın Adı:")
    publicationYear = StringField("Yayın Yılı:")
    publicationGender = StringField("Yayın Türü:")
    publicationPlace = StringField("Yayın Yeri:")

#Ad Soyad Form
class NameSurnameForm(Form): 
    name = StringField("Adı:")
    surname = StringField("Soyadı:")

#Yayın Adı-Yılı Form
class Sorgu(Form): 
    sorgu = StringField("Sorgu:")

app = Flask(__name__)
app.secret_key="yazlab3"

@app.route("/")
def index():
    return render_template("index.html")

#Admin Paneli
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        email = form.email.data
        password = form.password.data

        if email == "admin" and password == "admin":
            flash("Hoşgeldiniz", "success")
            session["admin"] = True
            return redirect(url_for("addWriter"))
        else:
            flash("Kullanıcı adı veya parola yanlış", "danger")
            return render_template("login.html", form = form)
    else:
        return render_template("login.html", form = form)

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

#Ad Soyad Sorgu
@app.route("/searchNameSurname", methods = ["GET", "POST"])
def searchNameSurname():
    form = NameSurnameForm(request.form)

    ad =  []
    soyad =  []
    yayinAdi =  []
    yayinYili =  []
    yayinTuru =  []
    yayinYeri =  []

    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data

        neo4j_create_statemenet = "Match((tur:TUR)<-[:YAYINLANIR]- (yayin:YAYIN) - [:YAYINYAZARI] -> (arastirmaci:ARASTIRMACI)) Where(arastirmaci.isim = '" + name + "' and arastirmaci.soyisim = '" + surname + "' ) return arastirmaci.isim as isim, arastirmaci.soyisim as soyisim, yayin.isim as yayinismi, yayin.yil as yil, tur.isim as tur, tur.yayinYeri as yayinYeri;"

        data_base_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "root"))
        session = data_base_connection.session()
        results = session.run(neo4j_create_statemenet)

        for result in results:
            ad.append(result["isim"])
            soyad.append(result["soyisim"])
            yayinAdi.append(result["yayinismi"])
            yayinTuru.append(result["tur"])
            yayinYili.append(result["yil"])
            yayinYeri.append(result["yayinYeri"])

        liste = []

        for i in range(len(ad)):
            liste.extend([[ad[i], soyad[i], yayinAdi[i], yayinYili[i], yayinTuru[i], yayinYeri[i]]])


        return render_template("searchNameSurname.html", form = form, liste = liste)
    
    return render_template("searchNameSurname.html", form = form)

#Yayın Adı Sorgu
@app.route("/searchPublicationName", methods = ["GET", "POST"])
def searchPublicationName():
    form = Sorgu(request.form)

    ad =  []
    soyad =  []
    yayinAdi =  []
    yayinYili =  []
    yayinTuru =  []
    yayinYeri =  []

    if request.method == "POST" and form.validate():
        sorgu = form.sorgu.data

        neo4j_create_statemenet = "Match((tur:TUR)<-[:YAYINLANIR]- (yayin:YAYIN) - [:YAYINYAZARI] -> (arastirmaci:ARASTIRMACI)) Where(yayin.isim = '" + sorgu + "') return arastirmaci.isim as isim, arastirmaci.soyisim as soyisim, yayin.isim as yayinismi, yayin.yil as yil, tur.isim as tur, tur.yayinYeri as yayinYeri;"

        data_base_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "root"))
        session = data_base_connection.session()
        results = session.run(neo4j_create_statemenet)

        for result in results:
            ad.append(result["isim"])
            soyad.append(result["soyisim"])
            yayinAdi.append(result["yayinismi"])
            yayinTuru.append(result["tur"])
            yayinYili.append(result["yil"])
            yayinYeri.append(result["yayinYeri"])

        liste = []

        for i in range(len(ad)):
            liste.extend([[ad[i], soyad[i], yayinAdi[i], yayinYili[i], yayinTuru[i], yayinYeri[i]]])


        return render_template("searchPublicationName.html", form = form, liste = liste)
    
    return render_template("searchPublicationName.html", form = form)

#Yayın Yılı Sorgu
@app.route("/searchPublicationYear", methods = ["GET", "POST"])
def searchPublicationYear():
    form = Sorgu(request.form)

    ad =  []
    soyad =  []
    yayinAdi =  []
    yayinYili =  []
    yayinTuru =  []
    yayinYeri =  []

    if request.method == "POST" and form.validate():
        sorgu = form.sorgu.data

        neo4j_create_statemenet = "Match((tur:TUR)<-[:YAYINLANIR]- (yayin:YAYIN) - [:YAYINYAZARI] -> (arastirmaci:ARASTIRMACI)) Where(yayin.yil = " + sorgu + ") return arastirmaci.isim as isim, arastirmaci.soyisim as soyisim, yayin.isim as yayinismi, yayin.yil as yil, tur.isim as tur, tur.yayinYeri as yayinYeri;"

        data_base_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "root"))
        session = data_base_connection.session()
        results = session.run(neo4j_create_statemenet)

        for result in results:
            ad.append(result["isim"])
            soyad.append(result["soyisim"])
            yayinAdi.append(result["yayinismi"])
            yayinTuru.append(result["tur"])
            yayinYili.append(result["yil"])
            yayinYeri.append(result["yayinYeri"])

        liste = []

        for i in range(len(ad)):
            liste.extend([[ad[i], soyad[i], yayinAdi[i], yayinYili[i], yayinTuru[i], yayinYeri[i]]])


        return render_template("searchPublicationYear.html", form = form, liste = liste)
    
    return render_template("searchPublicationYear.html", form = form)

#Yazar Ekleme
@app.route("/admin", methods = ["GET", "POST"])
def addWriter():
    form = WriterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        publicationName = form.publicationName.data
        publicationYear = form.publicationYear.data
        publicationGender = form.publicationGender.data
        publicationPlace = form.publicationPlace.data

        neo4j_create_statemenet = "create (arastirmaci:ARASTIRMACI{isim:'" + name +"', soyisim:'" + surname +"'}), (tur:TUR{isim:'" + publicationGender + "', yayinYeri:'" + publicationPlace + "'}), (yayin:YAYIN{isim:'" + publicationName + "', yil:" + publicationYear + "}), (yayin)-[:YAYINYAZARI]-> (arastirmaci), (yayin)-[:YAYINLANIR]-> (tur);"

        data_base_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "root"))
        session = data_base_connection.session()
        session.run(neo4j_create_statemenet)

    return render_template("admin.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)