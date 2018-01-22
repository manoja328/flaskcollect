from wtforms import Form, StringField, validators

class LoginForm(Form):
  username = StringField('Username:', validators=[validators.required(), validators.Length(min=1, max=30)])
  password = StringField('Password:', validators=[validators.required(), validators.Length(min=1, max=30)])
  email = StringField('Email:', validators=[validators.optional(), validators.Length(min=0, max=50)])
  
  
class QAForm(Form):
  question = StringField('question:', validators=[validators.required(), validators.Length(min=1, max=80)])
  answer =  StringField('answer:',  validators=[validators.required(), validators.Length(min=1, max=5)])
  filename = StringField('filename:', validators=[validators.required(), validators.Length(min=0, max=50)])