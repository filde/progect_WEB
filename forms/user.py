from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired



class UserForm(FlaskForm): # Форма для создания и редактирования профиля пользователя
    email = StringField('Почта', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Готово')