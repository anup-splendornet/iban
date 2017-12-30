from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from ibanproject import settings

def create_group():
    """Create Group and assign permission to group

    Create or get group by name.
    It will assign the permission of model Ibandata to this group

    Returns:
        object -- group object
        boolean -- false if there is error in any of the above process
    """
    try:
        # get all permissions of model ibandata
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #get or create group
        find_group = Group.objects.filter(name='Ibanadmin')
        if find_group:
            group = Group.objects.get(name='Ibanadmin')
        else:
            group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)
        return group
    except:
        return False

def permission_required(requested_permission):
    """Decorator for permission check

    It accepts permission name as parameter
    Created list of all permissions assigned to user and groups of all the users

    Arguments:
        requested_permission {[string]} -- name of the permission to check

    Returns:
        [class]  -- HttpResponseRedirect
        [object] -- view method object
    """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :
            user = request.user
            permissions = Permission.objects.values_list("codename",flat=True).filter(group__user=user)
            if requested_permission in permissions:
                return view_method(request, *args, **kwargs)
            else:
                messages.error(request, 'Insufficient Permissions.')
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return _arguments_wrapper
    return _method_wrapper