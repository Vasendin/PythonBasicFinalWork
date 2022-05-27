from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, Forganization, Faddorganization, Faddcontract, Faddfulfillment
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Organization, Contract, Fulfillment
from werkzeug.urls import url_parse
from random import randint
from datetime import date, timedelta, datetime


# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     return render_template('index.html', title='Домашняя страница')


# @app.route('/login', methods=['GET', 'POST'])
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

# cdate = datetime.today()+timedelta(days=15)
# print(str(cdate.month))
# print(str(datetime.today().month))
# print(str(cdate.month-datetime.today().month))

def fill():
    # for i in range(10):
    #     org = Organization(fullname='Organization {}'.format(i+1)
    #                        , name='Org. {}'.format(i+1)
    #                        , inn='290123456{}'.format(i)
    #                        , kpp='290101001'
    #                        , okpo='123456789{}'.format(i)
    #                        , head_position='генеральный директор'
    #                        , last_name='Петров'
    #                        , first_name='Петр'
    #                        , patronymic='Петрович'
    #                        , email='info@org{}.local'.format(i)
    #                        , accounting=True
    #                        )
    #     db.session.add(org)
    # db.session.commit()

    # contracts = db.session.query(Contract).all()
    # for i in contracts:
    #     db.session.delete(i)
    # db.session.commit()
    #
    # contractors = db.session.query(Organization).all()
    # for org in contractors:
    #     ncont = randint(2, 7)
    #     for i in range(ncont):
    #         cdate = datetime.today()-timedelta(days=randint(1, 200))
    #         end_date = datetime.today()+timedelta(days=randint(1, 500))
    #         contract = Contract(
    #                             start_date=cdate.date()
    #                             , end_date=end_date.date()
    #                             , date=cdate.date()
    #                             , number=str(randint(1, 10000))
    #                             , name='Контракт {}'.format(i+1)
    #                             , full_name='Контракт {}'.format(i+1)
    #                             , contractor=org.id
    #                             , price=randint(100000, 200000000)
    #                             )
    #         db.session.add(contract)
    # db.session.commit()

    contracts = db.session.query(Contract).all()
    for cont in contracts:
        nffm = randint(1, 7)
        start_date = cont.start_date
        ffm_date = last_day_of_month(cont.start_date)
        nmonths = cont.end_date.month - datetime.today().month
        totalprice = randint(15, 80)*cont.price/100
        for i in range(nmonths):
            fulfillment = Fulfillment(
                                      contract_id=cont.id
                                      , start_date=start_date
                                      , end_date=ffm_date
                                      , date=ffm_date
                                      , number=str(i+1)
                                      , price=round(totalprice/(nmonths+1)+randint(0,round(totalprice*0.05/(nmonths+1)))-randint(0,round(totalprice*0.05/(nmonths+1))),2)
            )
            start_date = ffm_date + timedelta(days=1)
            ffm_date = last_day_of_month(ffm_date + timedelta(days=15))
            print(str(fulfillment.start_date)+' '+str(fulfillment.end_date)+' '+fulfillment.number+' '+' '+str(fulfillment.price))
            db.session.add(fulfillment)
    db.session.commit()