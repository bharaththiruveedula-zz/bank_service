from app import app, db, auth, scheduler
from datetime import datetime
import pytz
if app.config.get("DB_TYPE", "SQL") == "SQL":
    from app import sql_utils as utils
else:
    from app import mongo_utils as utils


from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash


def transfer_balance_later(user, transfer_details):
    """
    :param user: SQLAlchemy object of the user
    :param transfer_details: dict which contains amount
    :return:None
    The task which runs by queue for future transactions
    """
    utils.transfer_balance_later(user, transfer_details)


def payee_exists(username, payee_name):
    user = utils.get_user(username)
    utils.get_payee_by_user(user, payee_name)
    return True


@auth.verify_password
def verify_password(username, password):
    return utils.verify_password(username, password)

@app.route('/')
@auth.login_required
def index():
  return 'Bank API Index Point. Please Login or Register'


@app.route('/register', methods=["POST"])
def register():
    user_info = request.json
    username = user_info["username"]
    hash = generate_password_hash(user_info["password"])
    email = user_info.get("email")
    balance = 0.0
    utils.register_user(username, email, hash, balance)
    return "Successfully registered"

@app.route('/balance', methods=['GET'])
@auth.login_required
def get_balance():
    user = utils.get_user(request.authorization["username"])
    return jsonify({"balance": user.balance})


@app.route('/transfer', methods=['POST'])
@auth.login_required
def transfer_balance():
    user = utils.get_user(request.authorization["username"])
    transfer_details = request.json
    if transfer_details.get("time"):
        t = datetime.strptime(transfer_details.get("time"), '%Y-%m-%d %H:%M:%S')
        scheduler.enqueue_at(t, transfer_balance_later, user, transfer_details)
        return "Transferring balance scheduled"
    if payee_exists(user.username, transfer_details["payee_name"]) and user.balance > transfer_details["amount"] :
        utils.transfer_balance(transfer_details, user)
        return "Successfully transferred!"
    else:
        return "Sorry don't have sufficient balance!"

@app.route('/add_beneficiary', methods=['POST'])
@auth.login_required
def add_beneficiary():
    payee_info = request.json
    user = utils.get_user(request.authorization["username"])
    utils.add_payee(payee_info, user)
    return "Successfully added beneficiary to the {user}".format(user=user.username)


@app.route('/delete_beneficiary', methods=['DELETE'])
@auth.login_required
def delete_beneficiary():
    payee_info = request.json
    payee = utils.get_payee(payee_info)
    utils.delete_payee(payee)
    return "Deleted the payee {user}".format(user=payee_info["name"])


@app.route('/balance', methods=['POST'])
@auth.login_required
def add_balance():
    user = utils.get_user(request.authorization["username"])
    amount = request.json["amount"]
    utils.add_balance(user, amount)
    return "Congratulations, balance was updated!"


@app.route('/transactions', methods=['GET'])
@auth.login_required
def get_transactions():
    user = utils.get_user(request.authorization["username"])
    transactions = utils.get_transactions(user)
    return jsonify(transactions)



