from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class ProjectsForm(FlaskForm): # Форма для создания и редактирования проекта
    title = StringField('Название', validators=[DataRequired()])
    count = IntegerField('Количество участников', validators=[DataRequired()])
    about = TextAreaField("О проекте")
    submit = SubmitField('Готово')
