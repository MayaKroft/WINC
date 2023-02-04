from peewee import *
from functools import partial

db = SqliteDatabase("betsy.db")

class Tag(Model):
    name = CharField(max_length=30)

    class Meta:
        database = db

class User(Model):
    name = CharField(max_length=60)
    address = CharField()
    email = CharField()
    billing = CharField()

    class Meta:
        constraints = [SQL('UNIQUE("name" COLLATE NOCASE, "email" COLLATE NOCASE)')]
        database = db


class Product(Model):
    name = CharField(max_length=100)
    user = ForeignKeyField(User, backref= 'products')
    description = CharField()
    price = DecimalField(decimal_places= 2)
    stock = IntegerField(constraints=[Check('stock > 0')])
    tags = ManyToManyField(Tag, backref= 'tag_p')

    class Meta:
        database = db

class Transaction(Model):
    seller = ForeignKeyField(User, constraints=[Check('seller_id != buyer_id')])
    buyer = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    amount = IntegerField(constraints=[Check('amount > 0')])

    class Meta:
            database = db


ProductTag = Product.tags.get_through_model()

db.create_tables((Tag, User,Product,Transaction, ProductTag ))

