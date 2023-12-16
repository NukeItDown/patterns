from flask_sqlalchemy import SQLAlchemy
from settings import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    token = db.Column(db.String(256), default="")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class SimilarProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    similar_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    identifynumber = db.Column(db.String(50), nullable=True, default=None)

    similar_products = relationship(
        'Product',
        secondary='similar_products',
        primaryjoin=(id == SimilarProducts.product_id),
        secondaryjoin=(id == SimilarProducts.similar_id),
        backref='related_products',
        foreign_keys='[SimilarProducts.product_id, SimilarProducts.similar_id]'
    )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('Product', secondary='order_product', backref='orders')
    order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
    )