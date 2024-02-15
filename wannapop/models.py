from . import db_manager as db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from .mixins import BaseMixin, SerializableMixin
from sqlalchemy.orm import relationship

class Product(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    seller_id = db.Column(db.Integer) #db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Category(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class User(db.Model, BaseMixin, UserMixin, SerializableMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(64))
    email_token = db.Column(db.String(20), unique=True, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BlockedUser(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = 'blocked_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    blocked_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlockedUser {self.user_id}>'

class BannedProducts(db.Model, BaseMixin):
    __tablename__ = 'banned_products'

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    product = db.relationship('Product', backref='banned_product', lazy=True)

    def __repr__(self):
        return f"<BannedProducts {self.product_id}>"


class Order(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    offer = db.Column(db.Numeric(precision=10, scale=2))
    created = db.Column(db.DateTime, server_default=func.now())

    # Unique constraint for product_id and buyer_id
    __table_args__ = (db.UniqueConstraint('product_id', 'buyer_id', name='uc_product_buyer'),)

    # Relationships
    product = relationship("Product", backref="orders")
    buyer = relationship("User", backref="orders")

class ConfirmedOrder(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "confirmed_orders"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())

    # Relationship
    order = relationship("Order", backref="confirmed_order", uselist=False)