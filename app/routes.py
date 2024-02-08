from flask import  request, render_template
import requests

from  app  import app
from .forms import SignupForm
from .forms import LoginForm
from .forms import ErgastForm


@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'


    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'welcome to pokemon thanks for sign up  {email} {password}'
    else:
        return render_template('signup.html', form=form)
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'welcome to pokemon {email} {password}'
    else:
        return render_template('login.html', form=form)
        
    



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
    

