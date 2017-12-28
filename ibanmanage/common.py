from django.contrib.auth.models import Group, Permission

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
