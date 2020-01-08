from api.models import database
from api.app.forms import RegistrationForm
from api.models.user import User
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, url_for, request


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data, role = form.role.data, theme = form.theme.data, password = form.password.data, password2 = form.password2.data)
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


