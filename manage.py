from poebot import create_app
from poebot.extensions import db
from flask_migrate import MigrateCommand, Migrate
from flask_script import (
    Server,
    Manager
)


manager = Manager(create_app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    """
    Populate a small db with some example entries.
    """

    from poebot.admin.models import AdminUser, Role
    from poebot.admin.enums import DefaultRole, PermissionName
    from poebot.constants import Gender

    db.drop_all()
    db.create_all()

    roles = DefaultRole.all()
    permissions = PermissionName.all()
    db_roles = []
    for r in roles:
        role = Role(r)
        if r == DefaultRole.SUPERADMIN.value:
            for permission in permissions:
                role.add_permission(permission)
        if r == DefaultRole.ADMIN.value:
            role.add_permission(PermissionName.VIEW_DASHBOARD)
        db.session.add(role)
        db_roles.append(role)

    db.session.commit()

    admins = [
        {
            'partner_id': 0,
            'name': 'John Smith',
            'email': 'admin',
            'password': 'test',
            'gender': Gender.Male.value,
            'roles': db_roles
        }
    ]

    for admin in admins:
        user = AdminUser(fullname=admin['name'], email=admin['email'],
                         password=admin['password'], gender=admin['gender'])
        user.add_roles(*db_roles)
        db.session.add(user)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
