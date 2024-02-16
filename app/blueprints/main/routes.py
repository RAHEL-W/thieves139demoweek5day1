from . import main
from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from  app.models import Pokemon, db

from flask_login import current_user




@main.route("/")
def home():
    return render_template('home.html')

@main.route('/user/<name>')
def user(name):
    return f'hello {name}'



def get_pokemon_info(pokemon_identifier):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_identifier}/"
    response = requests.get(url)
   
    if response.status_code == 200:
        data = response.json()
        base_stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        pokemon_info = {
            
            "name": data["name"],
            "ability": data["abilities"][0]["ability"]["name"],
            "base_experience": data["base_experience"],
            "sprite_img": data["sprites"]["front_shiny"],
            "base_hp": base_stats["hp"],
            "base_attack": base_stats["attack"],
            "base_defense": base_stats["defense"]
        }
        return pokemon_info
   
@main.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokemonForm()
    if  request.method == 'POST' and form.validate_on_submit():
        pokemon_identifier = form.name_or_id.data
        pokemons = get_pokemon_info(pokemon_identifier)
        if pokemons:
                new_pokemon = Pokemon(
                    name=pokemons["name"],
                    base_hp=pokemons["base_hp"],
                    base_attack=pokemons["base_attack"],
                    base_defense=pokemons["base_defense"],
                    sprite_img=pokemons["sprite_img"]
                )
                db.session.add(new_pokemon)
                db.session.commit()
                print("Pokemon data saved to database successfully!")
        else:
                print(f"Error: Unable to fetch data for {pokemon_identifier}")

        return render_template('pokemon.html', form=form, pokemons = pokemons)
        
    else:
       return render_template('pokemon.html', form=form)





@main.route('/my_pokemon', methods=['GET', 'POST'])
def My_Pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.is_authenticated:  # Check if user is logged in
            pokemon_identifier = form.name_or_id.data
            pokemon_info = get_pokemon_info(pokemon_identifier)
            if pokemon_info:
                new_pokemon = Pokemon(
                    name=pokemon_info["name"],
                    base_hp=pokemon_info["base_hp"],
                    base_attack=pokemon_info["base_attack"],
                    base_defense=pokemon_info["base_defense"],
                    sprite_img=pokemon_info["sprite_img"]
                )
                new_pokemon.catch_by.append(current_user)  
                db.session.add(new_pokemon)
                db.session.commit()
                print("Pokemon caught and saved to database successfully!")
                return redirect(url_for('main.my_pokemon'))  
                print(f"Error: Unable to fetch data for {pokemon_identifier}")
                flash("Error: Unable to catch Pokemon. Please try again.")
        else:
            flash("You need to be logged in to catch Pokemon.") 

    return render_template('my_pokemon.html', form=form)


@main.route('/team')
def team():
     my_pokemons = My_Pokemon.query.all()
     return render_template('team.html', my_pokemons=my_pokemons)
     

