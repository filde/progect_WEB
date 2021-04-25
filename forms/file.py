from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class File(FlaskForm): # Загрузка фото достижения пользователя
    title = StringField('Подпись к документу', validators=[DataRequired()])
    image = FileField('Добавить документ', validators=[DataRequired()])
    submit = SubmitField('Загрузить')