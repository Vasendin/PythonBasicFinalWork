from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Organization


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Вход')


class Forganization(FlaskForm):
    fullname = StringField('Полное наименование', validators=[DataRequired()])
    name = StringField('Наименование')
    inn = IntegerField('ИНН', validators=[DataRequired()])
    kpp = IntegerField('КПП')
    okpo = IntegerField('ОКПО')
    off_address = StringField('Юридический адрес')
    post_address = StringField('Почтовый адрес')
    head_position = StringField('Должность руководителя')
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    patronymic = StringField('Отчество')
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Записать')


class Faddorganization(Forganization, FlaskForm):
    def validate_fullname(self, fullname):
        org = Organization.query.filter_by(fullname=fullname.data).first()
        if org is not None:
            raise ValidationError('Please use a different fullname.')

    def validate_inn(self, inn):
        inn = Organization.query.filter_by(inn=inn.data).first()
        if inn is not None:
            raise ValidationError('Please use a different inn.')



class Faddcontract(FlaskForm):
    date = DateField('Дата')
    number = StringField('Номер')
    contractor = SelectField('Контрагент', coerce=int)
    name = StringField('Предмет контракта')
    price = FloatField('Цена контракта')
    end_date = DateField('Срок выполнения работ')
    submit = SubmitField('Записать')


class Faddfulfillment(FlaskForm):
    date = DateField('Дата')
    number = StringField('Номер')
    contract = SelectField('Контракт', coerce=int)
    price = FloatField('Сумма выполнения')
    submit = SubmitField('Записать')