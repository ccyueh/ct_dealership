from app import app, db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Address(db.Model):
    __tablename__ = 'address'

    address_id = db.Column(db.Integer, primary_key=True)
    street_num = db.Column(db.String(10))
    address_1 = db.Column(db.String(80))
    address_2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(12))

class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    phone = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now())

    address = db.relationship('Address', backref=db.backref('account', lazy='joined'))

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))

    address = db.relationship('Address', backref=db.backref('staff', lazy='joined'))

class Car(db.Model):
    __tablename__ = 'car'

    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    color = db.Column(db.String(20))
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))

    account = db.relationship('Account', backref=db.backref('car', lazy='joined'))

class Financing(db.Model):
    __tablename__ = 'financing'

    loan_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))
    credit_score = db.Column(db.Integer)
    loan_amount = db.Column(db.Numeric(8, 2))

    account = db.relationship('Account', backref=db.backref('financing', lazy='joined'))
    car = db.relationship('Car', backref=db.backref('financing', lazy='joined'))

class Insurance(db.Model):
    __tablename__ = 'insurance'

    insurance_id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(80))
    premium = db.Column(db.Numeric(7, 2))
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))

    car = db.relationship('Car', backref=db.backref('insurance', lazy='joined'))

class Maintenance(db.Model):
    __tablename__ = 'maintenance'

    maintenance_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))
    maintenance_desc = db.Column(db.String(500))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    date_started = db.Column(db.DateTime, default=datetime.now())
    date_finished = db.Column(db.DateTime)

    car = db.relationship('Car', backref=db.backref('maintenance', lazy='joined'))
    staff = db.relationship('Staff', backref=db.backref('maintenance', lazy='joined'))

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    payment_amount = db.Column(db.Numeric(8, 2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))

    car = db.relationship('Car', backref=db.backref('payment', lazy='joined'))

class MaintenancePayment(db.Model):
    __tablename__ = 'maintenance_payment'

    id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.maintenance_id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))

    maintenance = db.relationship('Maintenance', backref=db.backref('maintenance_payment', lazy='joined'))
    payment = db.relationship('Payment', backref=db.backref('maintenance_payment', lazy='joined'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(80), unique=True, index=True)
    password_hash = db.Column(db.String(256))

    # setup password hash methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # setup password check method
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# add user loader; finds correct user to login when login_user is called
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
