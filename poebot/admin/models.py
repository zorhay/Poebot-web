from flask_login import UserMixin
import secrets
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from .enums import DefaultRole, PermissionName
from ..utils import get_current_time
from ..extensions import db
from ..constants import Gender


def get_token():
    return secrets.token_hex(32)


user_role_table = db.Table('user_role', db.Model.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('admin_user.id')),
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                           )

role_permission_table = db.Table('role_permission', db.Model.metadata,
                                 db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                                 db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                                 )

user_permission_table = db.Table('user_permission', db.Model.metadata,
                                 db.Column('user_id', db.Integer, db.ForeignKey('admin_user.id')),
                                 db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                                 )


class Permission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True)

    @classmethod
    def get_or_create(cls, name):
        instance = db.session.query(cls).filter_by(name=name).first()
        if instance:
            return instance
        else:
            instance = cls(name=name)
            db.session.add(instance)
            return instance

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Permission {}>'.format(self.name)

    def __init__(self, name=''):
        self.name = name.lower()


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True)
    permissions = db.relationship('Permission', secondary=role_permission_table)

    def add_permission(self, permission):
        if isinstance(permission, PermissionName):
            permission = Permission.get_or_create(permission.value)
        elif isinstance(permission, str):
            permission = Permission.get_or_create(permission)

        self.permissions.append(permission)

    def has_permission(self, name):
        if isinstance(name, PermissionName):
            name = name.value
        name = name.lower()
        if name == DefaultRole.SUPERADMIN.value:
            return True
        for r in self.permissions:
            if r.name == name:
                return True
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __init__(self, name=''):
        self.name = name.lower()


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class AdminUser(db.Model, UserMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer(), nullable=False, default=Gender.Male.value)
    token = db.Column(db.String, nullable=False, unique=True, default=get_token)
    create_at = db.Column(db.DateTime(), nullable=False, default=get_current_time)
    update_at = db.Column(db.DateTime(), nullable=False, default=get_current_time, onupdate=db.func.current_timestamp())

    roles = db.relationship('Role', secondary=user_role_table)
    permissions = db.relationship('Permission', secondary=user_permission_table)

    active = db.Column(db.Boolean(), nullable=False, default=True)

    @property
    def password_t(self):
        pass

    @password_t.setter
    def password_t(self, value):
        if value:
            self.set_password(value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        pass_hash = hashlib.sha3_256(self.password.encode('utf-8')).hexdigest()
        pass_hash = pass_hash[:min(10, len(pass_hash))]
        return "{}.{}.{}".format(self.token, int(self.active), pass_hash)

    @classmethod
    def get_by_id(cls, cookie):
        if not isinstance(cookie, str):
            return None
        parts = cookie.split('.')
        if len(parts) != 3:
            return None
        try:
            user = cls.query.filter(cls.token == parts[0]).first()
        except ValueError:
            return None

        if not user:
            return None

        if not user.active:
            return None

        pass_hash = hashlib.sha3_256(user.password.encode('utf-8')).hexdigest()
        pass_hash = pass_hash[:min(10, len(pass_hash))]

        try:
            if parts[2] != pass_hash:
                return None
        except KeyError:
            return None

        return user

    def add_roles(self, *roles):
        self.roles.extend([role for role in roles if role not in self.roles])

    def has_role(self, name):
        if isinstance(name, DefaultRole):
            name = name.value
        name = name.lower()
        for r in self.roles:
            if r.name == name:
                return True
        return False

    def has_roles(self, names):
        return all(self.has_role(n) for n in names)

    def add_permission(self, permission):
        if isinstance(permission, PermissionName):
            permission = Permission.get_or_create(permission.value)
        elif isinstance(permission, str):
            permission = Permission.get_or_create(permission)

        self.permissions.append(permission)

    def has_permission(self, name):
        if isinstance(name, PermissionName):
            name = name.value
        name = name.lower()
        for p in self.permissions:
            if name == p.name:
                return True

        for r in self.roles:
            if r.has_permission(name):
                return True

        return False

    def __init__(self, fullname=None, email=None, password=None, phone=None, gender=Gender.Male.value, partner_id=0):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        if password:
            self.set_password(password)
        self.gender = gender
        self.partner_id = partner_id
        self.token = get_token()

    def __str__(self):
        return self.email
