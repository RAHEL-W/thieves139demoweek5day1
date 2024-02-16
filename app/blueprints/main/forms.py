from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired



class PokemonForm(FlaskForm):
    name_or_id = StringField('Name_or_id: ', validators=[DataRequired()])
    submit_btn = SubmitField('Search')

class My_PokemonForm(FlaskForm):
    # name_or_id = StringField('Name_or_id: ', validators=[DataRequired()])
    submit_btn = SubmitField('Catch')

