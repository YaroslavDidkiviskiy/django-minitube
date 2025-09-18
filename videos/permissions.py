from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):
	"""
	Read: all users
	Write/Update/Delete: either admin(is_staff or is_superuser) or owner
	"""
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_authenticated
	
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		
		user = request.user
		return (obj.author_id == getattr(user, 'id', None)) or user.is_staff or user.is_superuser
