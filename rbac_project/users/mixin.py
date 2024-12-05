from django.db.models import Q
from django.contrib.auth.models import Permission
from .constants import PAGE_SECTION_ACCESS_MAP

class RBACMixin:
    def __init__(self, request=None, view=None, **kwargs):
        self._request = request
        self._view = view
        self._method_action_map = {
            'GET': 'view',
            'POST': 'add',
            'PATCH': 'change',
            'DELETE': 'delete',
        }

    def has_feature_access(self):
        # Detailed debugging
        print("=== RBAC Permission Check ===")
        print(f"Request User: {self._request.user}")
        print(f"User Email: {self._request.user.email}")
        print(f"Is Authenticated: {self._request.user.is_authenticated}")
        
        # Check if user is authenticated
        if not self._request.user.is_authenticated:
            print("User is not authenticated")
            return False

        # Check view attributes
        if not hasattr(self._view, 'rbac_data'):
            if hasattr(type(self._view), 'rbac_data'):
                rbac_data = type(self._view).rbac_data
            else:
                print("No rbac_data found")
                return False
        else:
            rbac_data = self._view.rbac_data

        print(f"RBAC Data: {rbac_data}")

        page = rbac_data.get('page')
        feature = rbac_data.get('feature')

        print(f"Page: {page}, Feature: {feature}")

        if not (page and feature):
            print("Page or feature not specified")
            return False

        # Get page and feature map
        page_map = PAGE_SECTION_ACCESS_MAP.get(page)
        if page_map is None:
            print(f"No page map found for {page}")
            return False
    
        feature_map = page_map.get(feature)
        if feature_map is None:
            print(f"No feature map found for {feature}")
            return False
    
        # Get user permissions
        user_permissions = Permission.objects.filter(
            Q(user=self._request.user) | Q(group__user=self._request.user)
        ).values_list('codename', flat=True)
        
        print(f"User Permissions: {list(user_permissions)}")

        # Get method and required permission
        method_action = self._method_action_map[self._request.method]
        required_permission = feature_map.get(method_action)
        
        print(f"Method: {self._request.method}")
        print(f"Method Action: {method_action}")
        print(f"Required Permission: {required_permission}")

        # Check if permission exists and is in user permissions
        if not required_permission:
            print(f"No permission defined for {method_action}")
            return False

        permission_check = required_permission.split('.')[-1] in user_permissions
        print(f"Permission Check Result: {permission_check}")

        return permission_check

    def get_feature_access_map(
        self,
        user,
        all_sections=True,
        page=None,
        section=None
    ):
        user_permissions = Permission.objects.filter(
            Q(user=user) | Q(group__user=user)
        ).values_list('codename', flat=True)

        if all_sections:
            return {
                page_name: {
                    section_name: {
                        action: perm.split('.')[-1] in user_permissions
                        for action, perm in page_sections.items()
                    }
                    for section_name, page_sections in page_sections.items()
                }
                for page_name, page_sections in PAGE_SECTION_ACCESS_MAP.items()
            }

        if not page or not section:
            return {}

        page_map = PAGE_SECTION_ACCESS_MAP.get(page)
        if not page_map:
            return {}

        section_map = page_map.get(section)
        if not section_map:
            return {}
        
        return {
            action: perm.split('.')[-1] in user_permissions 
            for action, perm in section_map.items()
        }