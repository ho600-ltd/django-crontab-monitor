from django.utils.translation import gettext as _

import rest_framework_filters

from guardian.shortcuts import get_objects_for_user

from crontab_monitor.models import SelectOption, Inspection, AlertLog
from crontab_monitor.permissions import AlertLogPermission



class StatusSelectOptionFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = SelectOption
        fields = {
            "swarm": ("icontains", ),
            "value": ("icontains", ),
        }



class InspectionFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = Inspection
        fields = {
            "name": ("icontains", ),
            "function_note": ("icontains", ),
        }



def function_option_queryset_by_request_user(request):
    if request.user.is_superuser or request.user.is_staff:
        return Inspection.objects.all().order_by('id')
    else:
        return get_objects_for_user(
            request.user,
            AlertLogPermission.METHOD_PERMISSION_MAPPING['GET'],
            any_perm=True,
            with_superuser=True,
            accept_global_perms=False).order_by('id')



class AlertLogFilter(rest_framework_filters.FilterSet):
    inspection = rest_framework_filters.RelatedFilter(
        InspectionFilter,
        label=_('Inspection'),
        field_name="inspection",
        queryset=function_option_queryset_by_request_user)
    status = rest_framework_filters.RelatedFilter(
        StatusSelectOptionFilter,
        label=_('Status'),
        field_name="status",
        queryset=SelectOption.objects.filter(swarm='alert-log-status').order_by('value'))
    class Meta:
        model = AlertLog
        fields = {
            "create_time": ("gte", "lt"),
            "executed_end_time": ("gte", "lt"),
            "update_time": ("gte", "lt"),
            "executed_time_ymdhm": ("istartswith", ),
            "title": ("icontains", ),
            "mail_body": ("icontains", ),
            "object_id_list": ("icontains", ),
        }
