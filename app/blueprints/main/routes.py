from . import main
from flask import render_template, request, flash, url_for,  redirect
import requests
from .forms import PokemonForm
from  app.models import Pokemon, db, User, My_Pokemon 

from flask_login import current_user, login_required




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
        queried_poke = Pokemon.query.get(pokemon_identifier)
        if pokemons and not queried_poke:
                new_pokemon = Pokemon(
                    name=pokemons["name"],
                    base_hp=pokemons["base_hp"],
                    base_attack=pokemons["base_attack"],
                    base_defense=pokemons["base_defense"],
                    sprite_img=pokemons["sprite_img"]
                )
                db.session.commit()
                print("Pokemon data saved to database successfully!")
        else:
                
                
                print(f"Error: Unable to fetch data for {pokemon_identifier}")

        return render_template('pokemon.html', form=form, pokemons = pokemons)
        
    else:
       return render_template('pokemon.html', form=form)



     







# @main.route('/my/<name>')
# @login_required
# def my(name):
#     return f" hello  {name}"


# @main.route('/my_pokemon/<pokemon_name>')
# def my_pokemon(pokemon_name):
#      return f"work {pokemon_name}"
    
@main.route('/team')
def team():
    caught_pokemon = current_user.catch.all()
    return render_template('team.html', caught_pokemon=caught_pokemon)  

@main.route('/my_pokemon/<pokemon_name>')
@login_required
def my_pokemon(pokemon_name):
    user = User.query.get(current_user.id)
    pokemon = Pokemon.query.filter_by(name =pokemon_name).first()

    caught_pokemon = current_user.catch.all()
    if len(caught_pokemon)  < 6:
        if pokemon not in caught_pokemon :
            current_user.catch.append(pokemon)
            db.session.commit()
            
            flash(f'Successfully caught {pokemon.name}', 'success')
        else:
            flash(f'Error:  {pokemon.name}  already  caught  by  you ', 'warning')  
    else:
         flash(f'Error: {current_user.username} cant caught more than 5', 'warning')       
         return redirect(url_for('main.team')) 
    return redirect(url_for('main.pokemon')) 

@main.route('/remove/<pokemon_name>')
@login_required
def remove(pokemon_name):
     user=  User.query.get(current_user.id)
     pokemon= Pokemon.query.filter_by(name= pokemon_name).first()
     current_user.catch.remove(pokemon)
     db.session.commit()
     flash(f'Successfully remove {pokemon.name}', 'success')
     return redirect(url_for('main.team')) 


