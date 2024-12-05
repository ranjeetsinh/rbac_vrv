from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser, Profile, Task

def create_groups_and_permissions():
    # Create content types
    user_content_type = ContentType.objects.get_for_model(CustomUser)
    profile_content_type = ContentType.objects.get_for_model(Profile)
    task_content_type = ContentType.objects.get_for_model(Task)

    # User Permissions
    user_permissions = [
        Permission.objects.create(
            codename='can_view_profile_details',
            name='Can View Profile Details',
            content_type=user_content_type
        ),
        Permission.objects.create(
            codename='can_edit_profile_details',
            name='Can Edit Profile Details', 
            content_type=user_content_type
        )
    ]

    # Profile Permissions
    profile_permissions = [
        Permission.objects.create(
            codename='can_view_profile_picture',
            name='Can View Profile Picture',
            content_type=profile_content_type
        ),
        Permission.objects.create(
            codename='can_change_profile_picture',
            name='Can Change Profile Picture',
            content_type=profile_content_type
        )
    ]

    # Task Permissions
    task_permissions = [
        Permission.objects.create(
            codename='can_view_all_tasks',
            name='Can View All Tasks',
            content_type=task_content_type
        ),
        Permission.objects.create(
            codename='can_view_tasks',
            name='Can View Tasks',
            content_type=task_content_type
        ),
        Permission.objects.create(
            codename='can_create_tasks',
            name='Can Create Tasks',
            content_type=task_content_type
        ),
        Permission.objects.create(
            codename='can_edit_tasks',
            name='Can Edit Tasks',
            content_type=task_content_type
        ),
        Permission.objects.create(
            codename='can_delete_tasks',
            name='Can Delete Tasks',
            content_type=task_content_type
        )
    ]

    # Create Groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    user_group, _ = Group.objects.get_or_create(name='User')

    # Assign Permissions to Groups
    admin_group.permissions.set(
        user_permissions + profile_permissions + task_permissions
    )
    manager_group.permissions.set(
        [u for u in user_permissions if 'delete' not in u.codename] + 
        [p for p in profile_permissions if 'delete' not in p.codename] + 
        [t for t in task_permissions if 'delete' not in t.codename]
    )
    user_group.permissions.set(
        [p for p in user_permissions if 'view' in p.codename] + 
        [p for p in profile_permissions if 'view' in p.codename] + 
        [p for p in task_permissions if 'view' or 'create' in p.codename]
    )

    return {
        'groups': {
            'admin': admin_group,
            'manager': manager_group,
            'user': user_group
        },
        'permissions': {
            'user': user_permissions,
            'profile': profile_permissions,
            'task': task_permissions
        }
    }