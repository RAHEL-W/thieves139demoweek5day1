from flask import  request, render_template
import requests

from  app  import app
from .forms import LoginForm

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    else:
        return render_template('login.html', form=form)
    
    
    



def get_pokemon_info(pokemon_identifier):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_identifier}/"
    response = requests.get(url)
    # output = []
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            
            "name": data["name"],
            "ability": data["abilities"][0]["ability"]["name"],
            "base_experience": data["base_experience"],
            "sprite_url": data["sprites"]["front_shiny"]
        }
        return pokemon_info
   
    
    
    
    pokemon_identifier = []
    for pokemon in pokemon_identifier:

       pokemon_data = get_pokemon_info(pokemon)
    #    output.append(pokemon_data)

       if pokemon_data:
         print(pokemon_data)
       else:
        print(f"Error: Unable to fetch data for {pokemon_identifier}")    




@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if  request.method == 'POST':
        pokemon_identifier = request.form.get('name_or_id')
        pokemons = get_pokemon_info(pokemon_identifier)
        return render_template('ergast.html', pokemons = pokemons)
    else:
       return render_template('ergast.html')
    


