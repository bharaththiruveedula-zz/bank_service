from app import app
from app import db
if app.config.get("DB_TYPE", "SQL") == "SQL":
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        balance = db.Column(db.Float)

        def __repr__(self):
            return '<User {}>'.format(self.username)

    class Transaction(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        timestamp = db.Column(db.DateTime, index=True, unique=True)
        amount = db.Column(db.Float)

        def to_dict(self):
            transaction = {
                "timestamp": self.timestamp,
                "amount": self.amount
            }
            return transaction


    class Payee(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        name = db.Column(db.String(120), index=True, unique=True)
        account_no = db.Column(db.Integer, unique=True)

else:
    from app.mongo_models import  User, Transaction, Payee