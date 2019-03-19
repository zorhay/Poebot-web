# -*- coding: utf-8 -*-
from enum import Enum


class DefaultRole(Enum):
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'
    USER = 'user'

    @classmethod
    def all(cls):
        return [e.value for e in cls]


class PermissionName(Enum):
    VIEW = 'view'
    NEW = 'new'
    EDIT = 'edit'
    DELETE = 'delete'

    @classmethod
    def all(cls):
        return [e.value for e in cls]


class Gender(Enum):
    Male = 1
    Female = 2
    Other = 3

    @classmethod
    def members(cls):
        return [(e.value, e.name) for e in cls]

    @classmethod
    def format(cls, value):
        return cls(value).name


class AnonymousUser:
    is_active = False
    is_authenticated = False
    is_anonymous = True

    def get_id(self):
        return None

    def has_role(self, *args):
        return False

    def has_permission(self, *args):
        return False
