from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import BMIEntry
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
import logging

auth = Blueprint('auth', __name__)
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Thay đổi ở đây: loại bỏ weight và height
        weight = float(request.form.get('weight')) if request.form.get('weight') else None
        height = float(request.form.get('height')) if request.form.get('height') else None
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))  # Loại bỏ weight và height
            db.session.add(new_user)
            db.session.commit()
            
            # Thêm thông tin weight và height sau khi đối tượng User đã được tạo
            new_user.weight = weight
            new_user.height = height
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/bmi', methods=['POST'])
@login_required
def calculate_bmi():
    weight_str = request.form.get('weight')
    height_str = request.form.get('height')

    if not weight_str or not height_str:
        flash('Please provide weight and height.', category='error')
        return redirect(url_for('views.home'))

    try:
        weight = float(weight_str)
        height = float(height_str)
    except ValueError:
        flash('Invalid weight or height.', category='error')
        return redirect(url_for('views.home'))

    if weight <= 0 or height <= 0:
        flash('Weight and height must be positive.', category='error')
        return redirect(url_for('views.home'))

    bmi = round(weight / (height ** 2), 1)
    gender = request.form.get('gender')
    family_history = request.form.get('family_history')
    favc = request.form.get('favc')
    fcvc = int(request.form.get('fcvc'))
    ncp = int(request.form.get('ncp'))
    caec = request.form.get('caec')
    smoke = request.form.get('smoke')
    age_str = request.form.get('age')

    if not age_str:
        flash('Please provide your age.', category='error')
        return redirect(url_for('views.home'))

    try:
        age = int(age_str)
    except ValueError:
        flash('Invalid age.', category='error')
        return redirect(url_for('views.home'))

    bmi_entry = BMIEntry(weight=weight, height=height, bmi=bmi, age=age, gender=gender, family_history=family_history, favc=favc, fcvc=fcvc, ncp=ncp, caec=caec, smoke=smoke, user_id=current_user.id)
    db.session.add(bmi_entry)
    db.session.commit()

    return render_template('bmi_result.html', bmi=bmi)