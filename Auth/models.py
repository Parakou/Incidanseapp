from __init__ import bd
from flask_security import UserMixin, RoleMixin


class RolesUsers(bd.Model):
    __tablename__ = 'roles_users'
    id = bd.Column(bd.Integer(), primary_key=True)
    user_id = bd.Column('user_id', bd.Integer(), bd.ForeignKey('user.id'))
    role_id = bd.Column('role_id', bd.Integer(), bd.ForeignKey('role.id'))

class Role(bd.Model, RoleMixin):
    __tablename__ = 'role'
    id = bd.Column(bd.Integer(), primary_key=True)
    name = bd.Column(bd.String(80), unique=True)
    description = bd.Column(bd.String(255))

class User(bd.Model, UserMixin):
    __tablename__ = 'user'
    id = bd.Column(bd.Integer, primary_key=True)
    email = bd.Column(bd.String(255), unique=True)
    username = bd.Column(bd.String(255), unique=True, nullable=True)
    password = bd.Column(bd.String(255), nullable=False)
    last_login_at = bd.Column(bd.DateTime())
    current_login_at = bd.Column(bd.DateTime())
    last_login_ip = bd.Column(bd.String(100))
    current_login_ip = bd.Column(bd.String(100))
    login_count = bd.Column(bd.Integer)
    active = bd.Column(bd.Boolean())
    fs_uniquifier = bd.Column(bd.String(255), unique=True, nullable=False)
    confirmed_at = bd.Column(bd.DateTime())
    roles = bd.relationship('Role', secondary='roles_users',
                         backref=bd.backref('users', lazy='dynamic'))