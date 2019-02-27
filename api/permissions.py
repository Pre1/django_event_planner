from rest_framework.permissions import BasePermission


class IsEventOrg(BasePermission):
	message = "Please step aside."
	def has_object_permission(self, request, view, obj):
		# isOrg = request.user.organizer.first()
		return request.user.is_staff or request.user == obj.organized_by