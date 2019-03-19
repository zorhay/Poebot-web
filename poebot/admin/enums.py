from enum import Enum


class DefaultRole(Enum):
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'

    @classmethod
    def all(cls):
        return [e.value for e in cls]


class PermissionName(Enum):
    VIEW_DASHBOARD = "VIEW_DASHBOARD".lower()
    ACCESS_ADMINUSER_INFO = "ACCESS_ADMINUSER_INFO".lower()
    ACCESS_ROLE_INFO = "ACCESS_ROLE_INFO".lower()
    ACCESS_PERMISSION_INFO = "ACCESS_PERMISSION_INFO".lower()

    @classmethod
    def all(cls):
        return [e.value for e in cls]
