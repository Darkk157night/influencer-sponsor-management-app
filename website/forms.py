from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,FloatField,DateField,SelectField,HiddenField,TextAreaField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from website.models import User

class loginForm(FlaskForm):
    username = StringField(label='User name',validators=[DataRequired()])
    password = PasswordField(label='Enter password',validators=[DataRequired()])
    submit = SubmitField(label='sign-in')

class Register_admin(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username =username_to_check.data).first()
        if user:
            raise ValidationError('Username exists, please choose a new username')
        
    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_id=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email exists try again with new one')
        
    username = StringField('Admin username', validators=[DataRequired(), Length(min=2, max=150)])
    email_address = StringField('Email address', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class Register_influenceForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username =username_to_check.data).first()
        if user:
            raise ValidationError('Username exists, please choose a new username')
    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_id=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email exists try again with new one')
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email_address = StringField('Email address', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    category = StringField('Category', validators=[Length(max=100)])
    niche = StringField('Niche', validators=[Length(max=100)])
    reach = IntegerField('Reach', validators=[DataRequired()])
    submit = SubmitField('Register')

class Register_companyForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username =username_to_check.data).first()
        if user:
            raise ValidationError('Username exists, please choose a new username')
        
    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_id=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email exists try again with new one')
        
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email_address = StringField('Email address', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Company/Individual Name', validators=[DataRequired(), Length(min=2, max=150)])
    industry = StringField('Industry', validators=[Length(max=100)])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Register')

class create_campaign(FlaskForm):
    name = StringField('Title', validators=[DataRequired(),Length(min=10,max=50)])
    description = StringField('Description',validators=[DataRequired(),Length(min=10,max=150)])
    start_date = DateField('Start date',validators=[DataRequired()])
    end_date = DateField('End date',validators=[DataRequired()])
    category = StringField('Category',validators=[DataRequired(),Length(min=10,max=40)])
    niche = StringField('Niche',validators=[DataRequired(),Length(min=10,max=40)])
    budget = FloatField('Budget',validators=[DataRequired()])
    goals = StringField('Goals',validators=[DataRequired(),Length(min=10,max=100)])
    visibility = SelectField('Visibility',choices=["Private","Public"],validators=[DataRequired()])
    submit = SubmitField('create')

class AdRequestForm(FlaskForm):
    campaign_id = HiddenField('Campaign', validators=[DataRequired()])
    influencer_id = HiddenField('Influencer', validators=[DataRequired()])
    messages = TextAreaField('Messages')
    requirements = TextAreaField('Requirements')
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Submit')