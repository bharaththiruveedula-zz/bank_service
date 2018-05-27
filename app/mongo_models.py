from pymodm import MongoModel, fields

class User(MongoModel):
    email = fields.EmailField()
    username = fields.CharField()
    password_hash = fields.CharField()
    balance = fields.FloatField()

    class Meta:
        connection_alias = 'bank-app'

class Transaction(MongoModel):
    user_id = fields.ReferenceField(User)
    timestamp = fields.DateTimeField()
    amount = fields.FloatField()

    class Meta:
        connection_alias = 'bank-app'

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "amount": self.amount
        }

class Payee(MongoModel):
    user_id = fields.ReferenceField(User)
    name = fields.CharField()
    account_no = fields.IntegerField()

    class Meta:
        connection_alias = 'bank-app'