from rest_framework.permissions import BasePermission

class IsUserOrInSameOrganization(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the same as the requested user
        if obj == request.user:
            return True
        
        # Allow access if the user is in the same organization
        user_organisations = request.user.organisations.all()
        requested_user_organisations = obj.organisations.all()
        if user_organisations.intersection(requested_user_organisations).exists():
            return True
        
        return False
