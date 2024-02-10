from flask import  request, render_template, redirect, url_for,flash
import requests

from  app  import app
from .forms import SignupForm
from .forms import LoginForm
from .forms import ErgastForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user



@app.route("/")
def home():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'


    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user =User(username, email, password)
        new_user.save()
        flash('success thank  you for sign up', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):

          flash(f'wellcome {queried_user.username}', 'info')
          login_user(queried_user)
          return redirect(url_for('home'))
        else: 
            flash('incorrect username, email or password....try again',  'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))    



def get_pokemon_info(pokemon_identifier):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_identifier}/"
    response = requests.get(url)
   
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            
            "name": data["name"],
            "ability": data["abilities"][0]["ability"]["name"],
            "base_experience": data["base_experience"],
            "sprite_url": data["sprites"]["front_shiny"]
        }
        return pokemon_info
   
@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    form = ErgastForm()
    if  request.method == 'POST' and form.validate_on_submit():
        pokemon_identifier = form.name_or_id.data
        pokemons = get_pokemon_info(pokemon_identifier)
        return render_template('ergast.html', form=form, pokemons = pokemons)
        
    else:
       return render_template('ergast.html', form=form)
    

