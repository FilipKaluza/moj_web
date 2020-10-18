from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email



## FORM for contact
class contactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address. Please use following format: example@example.com')),
        DataRequired()])
    text = TextAreaField('Message', [
        DataRequired(),
        Length(min=4, message=('The minimum message lenght is at least 4 letters'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
