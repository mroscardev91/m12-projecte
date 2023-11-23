from flask import current_app
from flask_principal import RoleNeed, Permission
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, ActionNeed, Permission, Identity, AnonymousIdentity
from enum import Enum


class Role(str, Enum):
    wanner = "wanner"
    admin = "admin"
    moderator = "moderator"

class Action(str, Enum):
    edit = "update"
    view = "list and read"
    create = "create"
    delete = "delete"


__wanner_role_need = RoleNeed(Role.wanner)
__admin_role_need = RoleNeed(Role.admin)
__moderator_role_need = RoleNeed(Role.moderator)

__edit_action_need = ActionNeed(Action.edit)
__view_action_need = ActionNeed(Action.view)
__create_action_need = ActionNeed(Action.create)
__delete_action_need = ActionNeed(Action.delete)

# Permissions
require_wanner_role = Permission(__wanner_role_need)
require_admin_role = Permission(__admin_role_need)
require_moderator_role= Permission(__moderator_role_need)
require_admin_or_wanner_role = Permission(__wanner_role_need), Permission(__moderator_role_need)

require_edit_permission = Permission(__edit_action_need)
require_view_permission = Permission(__view_action_need)
require_create_permission = Permission(__create_action_need)
require_delete_permission = Permission(__delete_action_need)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        if current_user.role == Role.wanner:
            # Role needs
            identity.provides.add(__wanner_role_need)
            # Action needs
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
            identity.provides.add(__create_action_need)
            identity.provides.add(__delete_action_need)
        elif current_user.role == Role.admin:
            # Role needs
            identity.provides.add(__admin_role_need)
            # Action needs
            identity.provides.add(__view_action_need)
            identity.provides.add(__edit_action_need)
            identity.provides.add(__delete_action_need)
        elif current_user.role == Role.moderator:
            # Role needs
            identity.provides.add(__moderator_role_need)
            # Action needs
            identity.provides.add(__view_action_need)
            identity.provides.add(__delete_action_need)
        else:
            current_app.logger.debug("Unkown role")