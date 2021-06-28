from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateTimeLocalField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    system_code = StringField('System Code', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    system_code = StringField('System Code', validators=[DataRequired(), Length(min=2, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ConfigForm(FlaskForm):
    phase1_name = StringField('Growth Phase-I', validators=[DataRequired()])
    phase1_StartDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase1_EndDate = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase1_T_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase1_T_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase1_pH_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase1_pH_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()]) 
    phase1_tds_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase1_tds_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase1_light = DecimalField('hrs/day', places=2, validators=[DataRequired()])
    phase2_name = StringField('Growth Phase-II', validators=[DataRequired()])
    phase2_StartDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase2_EndDate = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase2_T_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase2_T_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase2_pH_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase2_pH_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()]) 
    phase2_tds_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase2_tds_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase2_light = DecimalField('hrs/day', places=2, validators=[DataRequired()])
    phase3_name = StringField('Growth Phase-III', validators=[DataRequired()])
    phase3_StartDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase3_EndDate = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    phase3_T_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase3_T_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase3_pH_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase3_pH_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()]) 
    phase3_tds_ll = DecimalField('Lower limit', places=2, validators=[DataRequired()])
    phase3_tds_ul = DecimalField('Upper limit', places=2, validators=[DataRequired()])
    phase3_light = DecimalField('hrs/day', places=2, validators=[DataRequired()])
    submit = SubmitField('Save')