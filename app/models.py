from app import db, login
from hashlib import md5
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    bmr = db.Column(db.Float)
    activity_f = db.Column(db.String(5))
    cal_req = db.Column(db.Float)
    exclude = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.weight = kwargs.get('weight')
        self.height = kwargs.get('height')
        self.dob = kwargs.get('dob')
        self.gender = kwargs.get('gender')
        self.name = kwargs.get('name')
        self.exclude = kwargs.get('exclude')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_age(self, dob, weight, height, gender, activity, wt_choice):
        today = date.today()
        self.age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        if gender == 'M':
            self.bmr = (10*weight) + (6.25*height) - (5*self.age) + 5
        elif gender == 'F':
            self.bmr = (10*weight) + (6.25*height) - (5*self.age) - 161

        if wt_choice == 'A':
            wt_mlt = 1
        elif wt_choice == 'B':
            wt_mlt = 0.87
        elif wt_choice == 'C':
            wt_mlt = 0.74
        elif wt_choice == 'D':
            wt_mlt = 0.48
        elif wt_choice == 'E':
            wt_mlt = 1.13
        elif wt_choice == 'F':
            wt_mlt = 1.26
        elif wt_choice == 'G':
            wt_mlt = 1.52

        if activity == '1.2':
            self.cal_req = self.bmr * 1.2 * wt_mlt
        elif activity == '1.375':
            self.cal_req = self.bmr * 1.375 * wt_mlt
        elif activity == '1.55':
            self.cal_req = self.bmr * 1.55 * wt_mlt
        elif activity == '1.725':
            self.cal_req = self.bmr * 1.725 * wt_mlt
        elif activity == '1.9':
            self.cal_req = self.bmr * 1.9 * wt_mlt

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_recipes(self):
        followed = Recipe.query.join(followers, (followers.c.followed_id == Recipe.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Recipe.query.filter_by(user_id=self.id)
        return followed.union(own)

