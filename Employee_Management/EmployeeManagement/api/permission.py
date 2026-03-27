from rest_framework.permissions import BasePermission

class IsBoss(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "BOSS"


class IsLeader(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "LEADER"


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MEMBER"