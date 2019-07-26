from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, ContactForm, LoginForm, RegisterForm, PostForm
from app.models import Post, Contact, User
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
@app.route('/index/<header>', methods=['GET'])
def index(header=''):
    return render_template('index.html', title='Home', products=products, header=header)

@app.route('/title', methods=['GET', 'POST'])
def title():
    # create an instance of the form
    form = TitleForm()

    # write a conditional that checks if form was submitted properly
    if form.validate_on_submit():
        return redirect(url_for('index', header=form.title.data))

    return render_template('form.html', form=form, title='Change Title')

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

        # if user does exist, and credentials are correct, log them in and send them to their profile page
        login_user(user, remember=form.remember_me.data)

        flash('You are now logged in.')
        return redirect(url_for('profile', username=current_user.username))

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
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = form.age.data,
            bio = form.bio.data
        )

        # set password hash
        user.set_password(form.password.data)

        # add to stage and commit
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering!')
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title='Register')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        contact = Contact(
            name = form.name.data,
            email = form.email.data,
            message = form.message.data
        )
        db.session.add(contact)
        db.session.commit()

        flash("Thanks for contacting us! We will be in touch soon.")

        return redirect(url_for('contact'))

    return render_template('form.html', form=form, title='Contact Us')

@login_required
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=''):
    form = PostForm()

    if form.validate_on_submit():
        # step 1: create an instance of the db model
        post = Post(
            tweet = form.tweet.data,
            user_id = current_user.id
        )

        # step 2: add the record to the stage
        db.session.add(post)

        # step 3: commit the stage to the db
        db.session.commit()

        return redirect(url_for('profile', username=username))

    # retrieve all posts and pass into view
    #posts = Post.query.all()

    # pass in user via the username taken in
    user = User.query.filter_by(username=username).first()

    return render_template('profile.html', form=form, user=user, title='Profile')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
