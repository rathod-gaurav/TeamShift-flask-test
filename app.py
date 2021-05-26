from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

from forms import LoginForm
from forms import RegistrationForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'b017acb0f2dea5916430f103839c0cd6'

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@teamshift.org' and form.password.data == 'TeamSHIFT2021' and form.system_code.data == 'SHIFT001':
            flash('You have been logged in to system!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful! Please check your credentials', 'warning')
    return render_template('login.html', title='Login', form=form)


@app.route("/systemhomepage")
def homepage():
    return render_template('homepage.html', title='Homepage')


if __name__ == '__main__':
    app.run(debug=True)