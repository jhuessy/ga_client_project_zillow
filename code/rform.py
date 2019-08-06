#IMPORTS
from wtforms import TextField, validators, SubmitField
from flask_wtf import FlaskForm

class ReusableForm(FlaskForm):
    # ZIPCODE TEXTFIELD WITH LENGTH = 5 VALIDATED
    zipcode = TextField("Enter a ZIPCode to see residential property values",
                        validators=[validators.InputRequired(),
                                    validators.Length(min=5,
                                                      max=5
                                                      )])
    # SUBMIT BUTTON
    submit = SubmitField("Enter")
