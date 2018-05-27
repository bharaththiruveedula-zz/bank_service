from datetime import datetime
import pytz

from app.mongo_models import User, Payee, Transaction
from werkzeug.security import check_password_hash

def verify_password(username, password):
    user = get_user(username)
    if user != None and check_password_hash(user.password_hash, password):
        return True
    return False

def register_user(username, email, password, amount):
    user = User(username=username, email=email, password_hash=password, balance=amount)
    user.save()

def get_user(user):
    try:
        user = User.objects.get({"username":user})
        return user
    except Exception as e:
        return None

def add_payee(payee_info, user):
    payee = Payee(user_id=User.objects.get({"_id": user._id}), name=payee_info["name"], account_no=payee_info["account_no"])
    payee.save()

def get_payee(payee_info):
    payee = Payee.objects.get({"name": payee_info["name"]})
    return payee

def get_payee_by_user(user, payee_name):
    payee = Payee.objects.get({"user_id":User.objects.get({"_id": user._id})})
    return payee

def delete_payee(payee):
    payee.delete()

def add_balance(user, amount):
    user.balance = user.balance + amount
    user.save()
    transaction = Transaction(user_id=User.objects.get({"_id": user._id}), timestamp=datetime.now(pytz.utc), amount=amount)
    transaction.save()


def get_transactions(user):
    transactions = Transaction.objects.raw({"user_id": user._id})
    return [transaction.to_dict() for transaction in transactions]

def transfer_balance(transfer_details, user):
    user.balance = user.balance - transfer_details["amount"]
    user.save()
    transaction = Transaction(user_id=User.objects.get({"_id": user._id}), timestamp=datetime.now(pytz.utc),
                              amount=(transfer_details["amount"]*-1))
    transaction.save()


def transfer_balance_later(user, transfer_details):
    user.balance = user.balance - transfer_details["amount"]
    user.save()
    transaction = Transaction(user_id=User.objects.get({"_id": user._id}), timestamp=datetime.now(pytz.utc),
                              amount=(transfer_details["amount"] * -1))
    transaction.save()
    # db_commit(user, transfer_details["amount"])
    print "Successfully transferred!"