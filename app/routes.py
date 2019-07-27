from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, RegisterForm, CustomerForm, MaintenanceForm
from app.models import User, Maintenance, Car
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # query the database fo the user trying to log in
        user = User.query.filter_by(email=form.email.data).first()

        # if user doesn't exist, reload page and flash message
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect.')
            return redirect(url_for('login'))

        # if user does exist, and credentials are correct, log them in and send them to the maintenance page
        login_user(user, remember=form.remember_me.data)

        flash('You are now logged in.')
        return redirect(url_for('maintenance'))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # check to see if user is already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data
        )

        # set password hash
        user.set_password(form.password.data)

        # add to stage and commit
        db.session.add(user)
        db.session.commit()

        flash('You are now registered.')
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title='Register')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = CustomerForm()

    if form.validate_on_submit():
        return redirect(url_for('/inventory', first=first, last=last, title='Cars')

    return render_template('form.html', form=form, title='Customer Lookup')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory(first='Goodcar', last='Dealership', title='Inventory'):
    
    rows = Car.query.join(Account, Car.account_id == Account.account_id).filter(Account.first_name == first, Account.last_name == last)

    return render_template('inventory.html', rows=rows, first=first, last=last, title=title)

@login_required
@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    form = MaintenanceForm()

    if form.validate_on_submit():
        maintenance = Maintenance(
            car_id = form.username.data,
            maintenance_desc = form.maintenance_desc.data,
            staff_id = form.staff_id.data,
            date_started = form.date_started.data,
            date_finished = form.date_finished.data
        )

        db.session.add(maintenance)
    
        db.session.commit()

        return redirect(url_for('maintenance'))

    return render_template('form.html', form=form, title='Maintenance')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
