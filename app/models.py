from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    #    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    inn = db.Column(db.String(12), index=True, unique=True)
    kpp = db.Column(db.String(9))
    okpo = db.Column(db.String(10))
    off_address = db.Column(db.String, index=True)
    post_address = db.Column(db.String, index=True)
    head_position = db.Column(db.String(30))
    last_name = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(32), index=True)
    patronymic = db.Column(db.String(32), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    accounting = db.Column(db.Boolean, index=True)
    contracts = db.relationship('Contract', backref='contracts', lazy='dynamic')

    def __repr__(self):
        return '<Organization {}>'.format(self.fullname)


class Typecontract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64), index=True, unique=True)
    we_sell = db.Column(db.Boolean, index=True)
    protected = db.Column(db.Boolean)

    def __repr__(self):
        return '<TypeContract {}>'.format(self.typename)


class Typefulfillment(db.Model):  # тип выполнения
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64), index=True, unique=True)
    protected = db.Column(db.Boolean)

    def __repr__(self):
        return '<TypeFulfillment {}>'.format(self.typename)


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('typecontract.id'))
    typefulfillment_id = db.Column(db.Integer, db.ForeignKey('typefulfillment.id'))
    accounting_method = db.Column(db.Integer)  # 1-по ед. расценкам, 2-по смете, 3-акт за машиночасы, 4-накладная
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price = db.Column(db.Float, index=True)
    contractor = db.Column(db.Integer, db.ForeignKey('organization.id'))
    number = db.Column(db.String(32), index=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    full_name = db.Column(db.String, index=True)
    fulfillments = db.relationship('Fulfillment', backref='contract', lazy='dynamic')


class Fulfillment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price = db.Column(db.Float, index=True)
    number = db.Column(db.String(32), index=True)
    date = db.Column(db.Date, index=True)
