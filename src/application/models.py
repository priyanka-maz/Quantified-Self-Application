from flask_security.core import UserMixin, RoleMixin
from .database import db


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id'))
                       )
                       
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    type = db.Column(db.String)
    mcq = db.Column(db.String)
    bstr = db.Column(db.String)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), nullable=False)
    timestamp = db.Column(db.String) 
    value = db.Column(db.String)
    note = db.Column(db.String) 
