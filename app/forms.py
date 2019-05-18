from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Bruger


class LoginForm(FlaskForm):
	brugernavn = wtforms.StringField('Brugernavn', validators=[DataRequired()])
	adgangskode = wtforms.PasswordField('Adgangskode', validators=[DataRequired()])
	husk_mig = wtforms.BooleanField('Husk')
	submit = wtforms.SubmitField('Log ind')


class OpretForm(FlaskForm):
    brugernavn = wtforms.StringField('Brugernavn', validators=[DataRequired()])
    email = wtforms.StringField('Email', validators=[DataRequired(), Email()])
    adgangskode = wtforms.PasswordField('Adgangskode', validators=[DataRequired()])
    adgangskode2 = wtforms.PasswordField(
        'Gentag adgangskode', validators=[DataRequired(), EqualTo('adgangskode')])
    submit = wtforms.SubmitField('Opret')

    def validate_username(self, brugernavn):
        bruger = Bruger.query.filter_by(brugernavn=brugernavn.data).first()
        if bruger is not None:
            raise ValidationError('Brug venligst et andet brugernavn.')

    def validate_email(self, email):
        bruger = Bruger.query.filter_by(email=email.data).first()
        if bruger is not None:
            raise ValidationError('Brug venligst en anden email.')
