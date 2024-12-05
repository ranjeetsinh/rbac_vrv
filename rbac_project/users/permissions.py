from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from users import constants

class IsTaskOwner(BasePermission):
    """
    Custom permission to check if the user has permission to change a task.
    """

    def has_permission(self, request, view):
        # Apply the permission only for methods that modify the task
        if request.user.has_perm(constants.CAN_VIEW_ALL_TASKS):
            print('//////////')
            return True
        if request.method in ['GET', 'PATCH', 'DELETE']:
            task = get_object_or_404(view.get_queryset(), pk = view.kwargs['pk'])

            # Check if the user has the CAN_CHANGE_TASK permission
            if request.user.has_perm(constants.CAN_CHANGE_TASK):
                task_created_by_id = task.created_by_id
                task_assigned_to = task.assignee_id
                lead_agent_id = task.lead.leadinfo.agent.id if task.lead.leadinfo.agent else None
                user_id = request.user.id

                if (
                    task_created_by_id == user_id
                    or task_assigned_to == user_id
                ):
                    return True
            return False
        
        return True