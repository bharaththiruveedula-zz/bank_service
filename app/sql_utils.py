from datetime import datetime
import pytz

from app.models import User, Payee, Transaction
from app import db
from werkzeug.security import check_password_hash, generate_password_hash

def verify_password(username, password):
    user = get_user(username)
    if user != None and check_password_hash(user.password_hash, password):
        return True
    return False

def register_user(username, email, password, amount):
    user = User(username=username, email=email, password_hash=password, balance=amount)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        return "Couldn't create user {user}, please try again after some time.".format(username)


def get_user(user):
    return User.query.filter_by(username=user).first_or_404()

def add_payee(payee_info, user):
    payee = Payee(user_id=user.id, name=payee_info["name"], account_no=payee_info["account_no"])
    db.session.add(payee)
    try:
        db.session.commit()
    except Exception as e:
        return "Couldn't add payee for {user}, please try again after some time.".format(user.username)

def get_payee(payee_info):
    payee = Payee.query.filter_by(name=payee_info["name"]).first_or_404()
    return payee

def get_payee_by_user(user, payee_name):
    payee = Payee.query.filter_by(user_id=user.id).filter_by(name=payee_name).first_or_404()
    return payee

def delete_payee(payee):
    db.session.delete(payee)
    try:
        db.session.commit()
    except Exception as e:
        return "Couldn't delete payee for {user}, please try again after some time.".format(user=payee_info["name"])

def add_balance(user, amount):
    user.balance = user.balance + amount
    transaction = Transaction(user_id=user.id, timestamp=datetime.now(pytz.utc), amount=amount)
    db.session.add(transaction)
    db.session.commit()

def get_transactions(user):
    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp).all()
    return [transaction.to_dict() for transaction in transactions]

def transfer_balance(transfer_details, user):
    user.balance = user.balance - transfer_details["amount"]
    transaction = Transaction(user_id=user.id, timestamp=datetime.now(pytz.utc), amount=(transfer_details["amount"]*-1))
    db.session.add(transaction)
    db.session.commit()

def transfer_balance_later(user, transfer_details):
    session = db.create_scoped_session()
    user.balance = user.balance - transfer_details["amount"]
    transaction = Transaction(user_id=user.id, timestamp=datetime.now(pytz.utc),
                              amount=(transfer_details["amount"] * -1))
    session.add(transaction)
    session.add(user)
    session.commit()
    # db_commit(user, transfer_details["amount"])
    print "Successfully transferred!"
