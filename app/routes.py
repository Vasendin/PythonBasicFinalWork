from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, Forganization, Faddorganization, Faddcontract, Faddfulfillment
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Organization, Contract, Fulfillment
from werkzeug.urls import url_parse
from app.filling import fill

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Домашняя страница')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/lists/contracts', methods=['GET', 'POST'])
@login_required
def contracts():
    # fill()
    c_list = Contract.query.all()
    org_list = Organization.query.all()
    ffm_list = Fulfillment.query.all()
    cont_ffm = []
    for i in c_list:
        ffm = 0
        for j in ffm_list:
            if j.contract_id == i.id:
                ffm = ffm + j.price
        cont_ffm.append((i.id, round(ffm, 2), round(ffm*100/i.price,1)))
    return render_template('lists/contracts.html', title='Контракты', list=c_list, org_list=org_list, cont_ffm=cont_ffm)


@app.route('/lists/contracts/add_contract', methods=['GET', 'POST'])
@login_required
def add_contract():
    contractors = db.session.query(Organization).all()
    #    types = Typemachinery.query.all()
    cont_list = [(i.id, i.name) for i in contractors]
    addform = Faddcontract()
    addform.contractor.choices = cont_list
    if addform.validate_on_submit():
        contract = Contract(date=addform.date.data,
                            number=addform.number.data,
                            contractor=addform.contractor.data,
                            name=addform.name.data,
                            price=addform.price.data,
                            end_date=addform.end_date.data)
        db.session.add(contract)
        db.session.commit()
        flash('Контракт добавлен')
        return redirect(url_for('contracts'))
    else:
        flash('Контракт не добавлен')
    return render_template('lists/add_row.html', title='Новый контракт', form=addform)


@app.route('/lists/contracts/<int:e_id>/edit_row', methods=['GET', 'POST'])
@login_required
def edit_contract(e_id):
    # row = request.form[e_id]
    erow = Contract.query.get(e_id)
    contractors = db.session.query(Organization).all()
    cont_list = [(i.id, i.name) for i in contractors]
    form1 = Faddcontract()
    form1.contractor.choices = cont_list
    if form1.date.data is None:
        form1.date.data = erow.date
    if form1.number.data is None:
        form1.number.data = erow.number
    if form1.contractor.data is None:
        form1.contractor.data = erow.contractor
    if form1.name.data is None:
        form1.name.data = erow.name
    if form1.price.data is None:
        form1.price.data = erow.price
    if form1.end_date.data is None:
        form1.end_date.data = erow.end_date

    if form1.validate_on_submit():
        erow.date = form1.date.data
        erow.number = form1.number.data
        erow.contractor = form1.contractor.data
        erow.name = form1.name.data
        erow.price = form1.price.data
        erow.end_date = form1.end_date.data
        db.session.commit()
        flash('Договор изменен')
        print(erow.name)
        return redirect(url_for('contracts'))
    else:
        flash('Договор не изменен')

    return render_template('lists/add_row.html', title='Изменить договор', form=form1)


@app.route('/lists/contracts/delete_row', methods=['GET', 'POST'])
@login_required
def delete_contract():
    row = request.form['del_id']
    drow = Contract.query.get(row)
    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('contracts'))


@app.route('/lists/organizations', methods=['GET', 'POST'])
def l_org():
    org = Organization.query.all()
    return render_template('lists/organizations.html', title='Контрагенты', org=org)


@app.route('/add_organization', methods=['GET', 'POST'])
@login_required
def add_org():
    form = Faddorganization()
    if form.validate_on_submit():
        org = Organization(fullname=form.fullname.data,
                           name=form.name.data,
                           inn=form.inn.data,
                           kpp=form.kpp.data,
                           okpo=form.okpo.data,
                           off_address=form.off_address.data,
                           post_address=form.post_address.data,
                           head_position=form.head_position.data,
                           last_name=form.last_name.data,
                           first_name=form.first_name.data,
                           patronymic=form.patronymic.data,
                           email=form.email.data)
        db.session.add(org)
        db.session.commit()
        flash('Контрагент добавлен')
        return redirect(url_for('l_org'))
    else:
        flash('Контрагент не добавлен')
    return render_template('lists/add_row.html', title='Новый контрагент', form=form)


@app.route('/lists/organizations/<int:e_id>/edit_row', methods=['GET', 'POST'])
@login_required
def edit_org(e_id):
    # row = request.form[e_id]
    erow = Organization.query.get(e_id)
    # contractors = db.session.query(Organization).all()
    # cont_list = [(i.id, i.name) for i in contractors]
    form1 = Forganization()
    # form1.contractor.choices = cont_list
    if form1.fullname.data is None:
        form1.fullname.data = erow.fullname
    if form1.name.data is None:
        form1.name.data = erow.name
    if form1.inn.data is None:
        form1.inn.data = erow.inn
    if form1.kpp.data is None:
        form1.kpp.data = erow.kpp
    if form1.okpo.data is None:
        form1.okpo.data = erow.okpo
    if form1.off_address.data is None:
        form1.off_address.data = erow.off_address
    if form1.post_address.data is None:
        form1.post_address.data = erow.post_address
    if form1.head_position.data is None:
        form1.head_position.data = erow.head_position
    if form1.last_name.data is None:
        form1.last_name.data = erow.last_name
    if form1.first_name.data is None:
        form1.first_name.data = erow.first_name
    if form1.patronymic.data is None:
        form1.patronymic.data = erow.patronymic
    if form1.email.data is None:
        form1.email.data = erow.email

    if form1.validate_on_submit():
        erow.fullname = form1.fullname.data
        erow.name = form1.name.data
        erow.inn = form1.inn.data
        erow.kpp = form1.kpp.data
        erow.okpo = form1.okpo.data
        erow.off_address = form1.off_address.data
        erow.post_address = form1.post_address.data
        erow.head_position = form1.head_position.data
        erow.last_name = form1.last_name.data
        erow.first_name = form1.first_name.data
        erow.patronymic = form1.patronymic.data
        erow.email = form1.email.data
        db.session.commit()
        flash('Организация изменена')
        print(erow.name)
        return redirect(url_for('l_org'))
    else:
        flash('Организация не изменена')

    return render_template('lists/add_row.html', title='Изменить организацию', form=form1)


@app.route('/lists/organizations/delete_row', methods=['GET', 'POST'])
@login_required
def delete_org():
    row = request.form['del_id']
    drow = Organization.query.get(row)
    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('l_org'))


@app.route('/lists/fulfillment', methods=['GET', 'POST'])
@login_required
def fulfillment():
    f_list = Fulfillment.query.all()
    # c_list = Contract.query.all()
    return render_template('lists/fulfillment.html', title='Выполнения', list=f_list)


@app.route('/lists/fulfillment/add_fulfillment', methods=['GET', 'POST'])
@login_required
def add_fulfillment():
    cont = db.session.query(Contract).all()
    #    types = Typemachinery.query.all()
    c_list = [(i.id, i.name) for i in cont]
    addform = Faddfulfillment()
    addform.contract.choices = c_list
    if addform.validate_on_submit():
        ffm = Fulfillment(date=addform.date.data,
                          number=addform.number.data,
                          contract_id=addform.contract.data,
                          price=addform.price.data
                          )
        db.session.add(ffm)
        db.session.commit()
        flash('Выполнение добавлено')
        return redirect(url_for('fulfillment'))
    else:
        flash('Выполнение не добавлено')
    return render_template('lists/add_row.html', title='Новое выполнение', form=addform)


@app.route('/lists/fulfillment/delete_row', methods=['GET', 'POST'])
@login_required
def delete_ffm():
    row = request.form['del_id']
    drow = Fulfillment.query.get(row)
    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('fulfillment'))
