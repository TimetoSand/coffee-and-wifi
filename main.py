from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)

bootstrap = Bootstrap(app)
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'any secret string'


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Integer, nullable=True)
    has_sockets = db.Column(db.Integer, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    open = TimeField('Opening time', validators=[DataRequired()])
    close = TimeField('Closing time', validators=[DataRequired()])
    coffee = SelectField('How was taste of coffee there?', validators=[DataRequired()], choices=[('☕☕☕☕☕', '☕☕☕☕☕'),
                                                                                                 ('☕☕☕☕', '☕☕☕☕'),
                                                                                                 ('☕☕☕', '☕☕☕'),
                                                                                                 ('☕☕', '☕☕'),
                                                                                                 ('☕', '☕')])
    price = StringField('How much is the coffee there?', validators=[DataRequired()], render_kw={"placeholder": "?£"})
    wifi = StringField('How strong is wifi? Rate 1-5')
    power = StringField('Can I charge my devices? Rate 1-5')
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    is_it_open = BooleanField('Is it still open?', validators=[DataRequired()])
    is_price_changed = BooleanField('Is price changed?', validators=[DataRequired()])
    price = StringField('New Price', render_kw={"placeholder": "?£"})
    submit = SubmitField('Submit')


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        print(request.form)
        return redirect("/")
    return render_template("add.html", form=form)


@app.route("/update", methods=["GET", "POST"])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        print(form.data)
        return redirect("/")
    return render_template("update.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)


