from flask_admin import consts as flask_admin_consts
import flask_admin as admin
from .admin_views import PoebotAdminIndexView

admin = admin.Admin(name='Poebot',
                    index_view=PoebotAdminIndexView(
                        url='/manage',
                        menu_icon_type=flask_admin_consts.ICON_TYPE_GLYPH,
                        menu_icon_value='glyphicon glyphicon-home'
                        ),
                    template_mode='bootstrap3'
                    )


