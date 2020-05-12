import csv
from datetime import datetime
from flask import Flask, render_template, flash , url_for ,redirect, jsonify, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY']='6ds4ds44sd4v5ds4f5sd1vvs5casda5s'

class RegistrationForm(FlaskForm):
    username = StringField('Pseudo',
                           validators=[DataRequired(), Length(min=6, max=18)])
    email = StringField('Adresse Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=5, max=22)])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enregistrez-vous')

class LoginForm(FlaskForm):
    email = StringField('Adresse Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connectez-vous')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/firstpage.html')
def firstpage():
    return render_template('firstpage.html')


@app.route('/secondpage.html')
def secondpage():
    return render_template('secondpage.html')


@app.route('/thirdpage.html')
def thirdpage():
    return render_template('thirdpage.html')





@app.route('/fifthpage.html', methods=['GET', 'POST'])
def fifthpage():
    form = RegistrationForm()
    if form.validate_on_submit():
        with open('data/website1.csv', 'a') as f:
            writer = csv.writer(f)

            writer.writerow([form.username.data, form.email.data, form.password.data])
        flash(f'le compte de  {form.username.data} a ete cree!', 'success')
        return redirect(url_for('index'))
    return render_template('fifthpage.html', title='Register', form=form)


@app.route('/sixthpage.html', methods=['GET', 'POST'])
def sixthpage():
    form = LoginForm()
    if form.validate_on_submit():
        with open('data/website1.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                if form.email.data == line[1] and form.password.data == line[2]:
                    flash(f'bienvenue {form.email.data} vous etes connecte !', 'success')
                    return redirect(url_for('seventhpage'))
                next(reader)
        flash('connexion echouee veuillez checker votre email et mot de passe', 'danger')
    return render_template('sixthpage.html', title='Login', form=form)


@app.route('/seventhpage.html', methods=['GET', 'POST'])
def seventhpage():
    return render_template('seventhpage.html')

@app.route('/<day>/<hour>', methods=['GET', 'POST'])
def meeting(day, hour):
    time = Time(day=day, hour=hour)
    db.session.add(time)
    db.session.commit()
    return ("added new time!")

@app.route('/fourthpage.html', methods=['GET', 'POST'])
def fourthpage():

    return render_template('fourthpage.html')

@app.route('/list')
def list():
    usernames=[]
    with open('data/website1.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            x=line[0]
            usernames.append(x)
            print(line)
            next(reader)
    with open('templates/eigthpage.html', 'w') as f1:
        s1 = "{% extends 'index.html' %} {% block body %} <ol> "
        for name in usernames:
            print(name)
            s1=s1+"<li>"+name+"</li>"
        s1 = s1 + "</ol> {% endblock %}"
        print(s1)
        f1.write(s1)
    return render_template("eigthpage.html")



if __name__ == '__main__':

    app.run(debug=True)
