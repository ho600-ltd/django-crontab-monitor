import logging

from django.db.models import Q

from rest_framework.permissions import BasePermission, SAFE_METHODS

from guardian.shortcuts import get_objects_for_user


from crontab_monitor.models import AlertLog



class SelectOptionPermission(BasePermission):
    METHOD_PERMISSION_MAPPING = {
        "POST": (),
        "GET": ("crontab_monitor.view_inspection", "crontab_monitor.edit_inspection", ),
        "PATCH": (),
        "DELETE": (),
    }


    def has_permission(self, request, view):
        return get_objects_for_user(request.user,
                                    self.METHOD_PERMISSION_MAPPING[request.method],
                                    any_perm=True,
                                    with_superuser=True,
                                    accept_global_perms=False,
                                   ).exists()


    def has_object_permission(self, request, view, obj):
        return get_objects_for_user(request.user,
                                    self.METHOD_PERMISSION_MAPPING[request.method],
                                    any_perm=True,
                                    with_superuser=True,
                                    accept_global_perms=False,
                                   ).exists()
                                  


class InspectionPermission(BasePermission):
    METHOD_PERMISSION_MAPPING = {
        "POST": (),
        "GET": ("crontab_monitor.view_inspection", "crontab_monitor.edit_inspection", ),
        "PATCH": ("crontab_monitor.edit_inspection", ),
        "DELETE": (),
    }


    def has_permission(self, request, view):
        return get_objects_for_user(request.user,
                                    self.METHOD_PERMISSION_MAPPING[request.method],
                                    any_perm=True,
                                    with_superuser=True,
                                    accept_global_perms=False,
                                   ).exists()


    def has_object_permission(self, request, view, obj):
        return obj in get_objects_for_user(request.user,
                                           self.METHOD_PERMISSION_MAPPING[request.method],
                                           any_perm=True,
                                           with_superuser=True,
                                           accept_global_perms=False,
                                          )



class AlertLogPermission(BasePermission):
    METHOD_PERMISSION_MAPPING = {
        "POST": (),
        "GET": ("crontab_monitor.view_alert_log", "crontab_monitor.edit_alert_log", ),
        "PATCH": (),
        "DELETE": (),
    }


    def has_permission(self, request, view):
        return get_objects_for_user(request.user,
                                     self.METHOD_PERMISSION_MAPPING[request.method],
                                     any_perm=True,
                                     with_superuser=True,
                                     accept_global_perms=False
                                    ).exists()
        


    def has_object_permission(self, request, view, obj):
        inspections = get_objects_for_user(request.user,
                                           self.METHOD_PERMISSION_MAPPING[request.method],
                                           any_perm=True,
                                           with_superuser=True,
                                           accept_global_perms=False,
                                          )
        return obj.inspection in inspections