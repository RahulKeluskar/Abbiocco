from app import db, login
from hashlib import md5
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, autoincrement=True,primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True,unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'),lazy='dynamic')
	def __init__(self,username,email):
		self.username = username
		self.email = email
	
	def __repr__(self):
		return '<User {}>'.format(self.username)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self,size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self,user):
		if self.is_following(user):
			self.followed.remove(user)
	def is_following(self, user):
		return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
	def followed_recipes(self):
		followed = Recipe.query.join(followers, (followers.c.followed_id == Recipe.user_id)).filter(followers.c.follower_id == self.id)
		own = Recipe.query.filter_by(user_id=self.id)
		return followed.union(own)
class Recipe(db.Model):
	__tablename__ = 'recipes'

	recipe_id = db.Column(db.String(64),nullable=False, primary_key=True)
	recipe_name = db.Column(db.String(200), nullable=True)
	img_url = db.Column(db.String(1000),nullable = True)
	instructions = db.Column(db.String(1000), nullable=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

	# Relationships

	cuisines = db.relationship("Cuisine",secondary="recipe_cuisines",backref=db.backref("recipes"))
	users = db.relationship("User",secondary="bookmarks",backref=db.backref("recipes"))

	def __repr__(self):
		return """<Recipe recipe_id={} recipe_name={} img_url={}
                  instructions={} user={}>""".format(self.recipe_id, self.recipe_name,
                                             self.img_url, self.instructions, self.user_id)

class Ingredient(db.Model):
	__tablename__ = 'ingredients'

	ing_id = db.Column(db.String(64), nullable=False, primary_key=True)
	ing_name = db.Column(db.String(64),nullable=False)

	def __repr__(self):
		return "<Ingredient ing_id={} ing_name={}>".format(self.ing_id,self.ing_name)

class List(db.Model):
	__tablename__='lists'

	list_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	list_name = db.Column(db.String(60),nullable=True)

	user = db.relationship("User", backref=db.backref("lists"))

	def __repr__(self):
		return "<List list_id={} user_id={} list_name={}>".format(self.list_id, self.user_id, self.list_name)
class Cuisine(db.Model):
	__tablename__ = 'cuisines'

	cuisine_id = db.Column(db.Integer,autoincrement=True,
		primary_key=True)
	cuisine_name = db.Column(db.String(60),nullable=True)

	def __repr__(self):
		return "<Cuisine cuisine_id={} cuisine_name={}>".format(
            self.cuisine_id, self.cuisine_name)
class RecipeIngredient(db.Model):
	__tablename__ = "recipe_ingredients"
	r_i_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))
	ing_id = db.Column(db.String(64), db.ForeignKey('ingredients.ing_id'))
	meas_unit = db.Column(db.String(30), nullable=True)
	mass_qty = db.Column(db.Integer, nullable=True)  # NOT to be incremented
	recipe = db.relationship("Recipe", backref="recipe_ingredients")
	ingredient = db.relationship("Ingredient", backref="recipe_ingredients")
	def __repr__(self):
		return """<RecipeIngredient r_i_id={} recipe_id={} ing_id={} meas_unit={} mass_qty={}>""".format(self.r_i_id, self.recipe_id,self.ing_id, self.meas_unit,self.mass_qty)
class ListIngredient(db.Model):
	__tablename__ = "list_ingredients"
	l_i_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
	list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'))
	ing_id = db.Column(db.String(64), db.ForeignKey('ingredients.ing_id'))
	meas_unit = db.Column(db.String(30), nullable=True)
	mass_qty = db.Column(db.Integer, nullable=True)  # incrementable
	lst = db.relationship("List", backref="list_ingredients")
	ingredient = db.relationship("Ingredient", backref='list_ingredients')
	def __repr__(self):
		return """<ListIngredient l_i_id={} list_id={} ing_id={} meas_unit={} mass_qty={}>""".format(self.l_i_id, self.list_id,
                                                      self.ing_id, self.meas_unit,
                                                      self.mass_qty)
class Bookmark(db.Model):
	__tablename__ = "bookmarks"
	bookmark_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))
	def __repr__(self):
		return """<Bookmark bookmark_id={} user_id={} recipe_id={}>""".format(
            self.bookmark_id, self.user_id, self.recipe_id)

class RecipeCuisine(db.Model):
	__tablename__ = "recipe_cuisines"
	recipe_cuisine_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
	cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
	recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))
	def __repr__(self):
		return "<RecipeCuisine recipe_cuisine_id={} cuisine_id={} recipe_id={}>".format(
            self.recipe_cuisine_id, self.cuisine_id, self.recipe_id)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))