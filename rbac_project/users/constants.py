PAGE_SECTION_ACCESS_MAP = {
        'profile': {
            'profile_details': {
                'view': 'auth.can_view_profile_details',
                'edit': 'auth.can_edit_profile_details',
            },
            'profile_picture': {
                'view': 'auth.can_view_profile_picture',
                'change': 'auth.can_change_profile_picture',
            }
        },
        'tasks': {
            'task_list': {
                'view': 'task.can_view_tasks',
                'add': 'task.can_create_tasks',
                'change': 'task.can_edit_tasks',
                'delete': 'task.can_delete_tasks'
            }
        }
    }

CAN_CHANGE_TASK = 'users.change_task'
CAN_VIEW_ALL_TASKS = 'users.can_view_all_tasks'