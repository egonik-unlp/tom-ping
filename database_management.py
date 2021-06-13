from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime



app=Flask(__name__)

db_name="database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(db_name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db=SQLAlchemy(app)

class Token(db.Model):
	__tablename__="token"
	token_id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String)
	offers=db.relationship("Offer", backref="token")
	token_values_usd=db.relationship("Token_Value_Usd", backref="token")
	def __init__(self,name):
		self.name=name
class Offer(db.Model):
	__tablename__="offer"
	offer_id=db.Column(db.Integer, nullable=False, primary_key=True )
	value_ars=db.Column(db.Float, nullable=False)
	date=db.Column(db.DateTime, nullable=False)
	token_id=db.Column(db.Integer, db.ForeignKey("token.token_id"), nullable=False)
	def __init__(self, value, token_id):
		self.value_ars=value
		self.date=datetime.now()
		self.token_id=token_id

class Token_Value_Usd(db.Model):
	__tablename__="token_value_usd"
	value_id=db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
	date=db.Column(db.DateTime, nullable=False)
	value_usd=db.Column(db.Float, nullable=True)
	token_id=db.Column(db.Integer, db.ForeignKey("token.token_id"), nullable=False)
	def __init__(self, date, value_usd, token_id):
		self.date=datetime.now()
		self.value_usd=value_usd
		self.token_id=token_id




