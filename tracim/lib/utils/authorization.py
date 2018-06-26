# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
import functools
from pyramid.interfaces import IAuthorizationPolicy
from zope.interface import implementer
try:
    from json.decoder import JSONDecodeError
except ImportError:  # python3.4
    JSONDecodeError = ValueError

from tracim.exceptions import InsufficientUserWorkspaceRole
from tracim.exceptions import InsufficientUserProfile
if TYPE_CHECKING:
    from tracim import TracimRequest
###
# Pyramid default permission/authorization mecanism

# INFO - G.M - 12-04-2018 - Setiing a Default permission on view is
#  needed to activate AuthentificationPolicy and
# AuthorizationPolicy on pyramid request
TRACIM_DEFAULT_PERM = 'tracim'


@implementer(IAuthorizationPolicy)
class AcceptAllAuthorizationPolicy(object):
    """
    Empty AuthorizationPolicy : Allow all request. As Pyramid need
    a Authorization policy when we use AuthentificationPolicy, this
    class permit use to disable pyramid authorization mecanism with
    working a AuthentificationPolicy.
    """
    def permits(self, context, principals, permision):
        return True

    def principals_allowed_by_permission(self, context, permission):
        raise NotImplementedError()

###
# Authorization decorators for views

# INFO - G.M - 12-04-2018
# Instead of relying on pyramid authorization mecanism
# We prefer to use decorators


def require_same_user_or_profile(group: int):
    """
    Decorator for view to restrict access of tracim request if candidate user
    is distinct from authenticated user and not with high enough profile.
    :param group: value from Group Object
    like Group.TIM_USER or Group.TIM_MANAGER
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, context, request: 'TracimRequest'):
            auth_user = request.current_user
            candidate_user = request.candidate_user
            if auth_user.user_id == candidate_user.user_id or \
                    auth_user.profile.id >= group:
                return func(self, context, request)
            raise InsufficientUserProfile()
        return wrapper
    return decorator


def require_profile(group: int):
    """
    Decorator for view to restrict access of tracim request if profile is
    not high enough
    :param group: value from Group Object
    like Group.TIM_USER or Group.TIM_MANAGER
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, context, request: 'TracimRequest'):
            user = request.current_user
            if user.profile.id >= group:
                return func(self, context, request)
            raise InsufficientUserProfile()
        return wrapper
    return decorator


def require_workspace_role(minimal_required_role: int):
    """
    Restricts access to endpoint to minimal role or raise an exception.
    Check role for current_workspace.
    :param minimal_required_role: value from UserInWorkspace Object like
    UserRoleInWorkspace.CONTRIBUTOR or UserRoleInWorkspace.READER
    :return: decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, context, request: 'TracimRequest'):
            user = request.current_user
            workspace = request.current_workspace
            if workspace.get_user_role(user) >= minimal_required_role:
                return func(self, context, request)
            raise InsufficientUserWorkspaceRole()

        return wrapper
    return decorator


def require_candidate_workspace_role(minimal_required_role: int):
    """
    Restricts access to endpoint to minimal role or raise an exception.
    Check role for candidate_workspace.
    :param minimal_required_role: value from UserInWorkspace Object like
    UserRoleInWorkspace.CONTRIBUTOR or UserRoleInWorkspace.READER
    :return: decorator
    """
    def decorator(func):

        def wrapper(self, context, request: 'TracimRequest'):
            user = request.current_user
            workspace = request.candidate_workspace

            if workspace.get_user_role(user) >= minimal_required_role:
                return func(self, context, request)
            raise InsufficientUserWorkspaceRole()

        return wrapper
    return decorator
