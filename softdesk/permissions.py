from rest_framework.permissions import BasePermission

from softdesk.models import Contributor


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.user == request.user


class CreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.creator == request.user


# todo cet héritage est-il vraiment utile ? Ne peut-on pas directement vérifer dans cette classe ?
class ProjectPermission(CreatorPermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            contributor = Contributor.objects.filter(user=request.user, project=obj)

            return len(contributor) > 0 and super().has_object_permission(request, view, obj)

        return super().has_object_permission(request, view, obj)


class ContributorPermission(UserPermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            contributor = Contributor.objects.filter(user=request.user, project=obj.project)

            return len(contributor) > 0 and super().has_object_permission(request, view, obj)

        return super().has_object_permission(request, view, obj)
