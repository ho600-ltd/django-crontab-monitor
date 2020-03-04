import logging
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, filters
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
import rest_framework_filters

from guardian.shortcuts import get_objects_for_user

from crontab_monitor.paginations import TenTo100PerPagePagination
from crontab_monitor.models import SelectOption, Inspection, AlertLog, single_entry_point
from crontab_monitor.filters import AlertLogFilter
from crontab_monitor.renderers import CMBrowsableAPIRenderer
from crontab_monitor.permissions import SelectOptionPermission, InspectionPermission, AlertLogPermission
from crontab_monitor.serializers import SelectOptionSerializer, InspectionSerializer, AlertLogSerializer



class SelectOptionModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, SelectOptionPermission, )
    queryset = SelectOption.objects.all()
    serializer_class = SelectOptionSerializer
    pagination_class = TenTo100PerPagePagination
    renderer_classes = (CMBrowsableAPIRenderer, JSONRenderer, )
    http_method_names = ('get', )


    def get_queryset(self):
        if get_objects_for_user(self.request.user,
                                SelectOptionPermission.METHOD_PERMISSION_MAPPING[self.request.method],
                                any_perm=True,
                                with_superuser=True,
                                accept_global_perms=False,
                               ).exists():
            return SelectOption.objects.all()
        else:
            return SelectOption.objects.none()



class InspectionModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, InspectionPermission, )
    queryset = Inspection.objects.none()
    serializer_class = InspectionSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('id', )
    default_ordering_fields = ('-id', )
    pagination_class = TenTo100PerPagePagination
    renderer_classes = (CMBrowsableAPIRenderer, JSONRenderer, )
    http_method_names = ('get', 'patch', )


    def get_queryset(self):
        return get_objects_for_user(self.request.user,
                                    InspectionPermission.METHOD_PERMISSION_MAPPING[self.request.method],
                                    any_perm=True,
                                    with_superuser=True,
                                    accept_global_perms=False,
                                   ).order_by(*self.default_ordering_fields)



class AlertLogModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, AlertLogPermission, )
    queryset = AlertLog.objects.none()
    serializer_class = AlertLogSerializer
    filterset_class = AlertLogFilter
    filter_backends = (filters.OrderingFilter, rest_framework_filters.backends.RestFrameworkFilterBackend)
    ordering_fields = ('id', )
    default_ordering_fields = ('-id', )
    pagination_class = TenTo100PerPagePagination
    renderer_classes = (CMBrowsableAPIRenderer, JSONRenderer, )
    http_method_names = ('get', )


    def get_queryset(self):
        inss = get_objects_for_user(self.request.user,
                                    AlertLogPermission.METHOD_PERMISSION_MAPPING[self.request.method],
                                    any_perm=True,
                                    with_superuser=True,
                                    accept_global_perms=False,
                                   )
        return AlertLog.objects.filter(inspection__in=inss).order_by(*self.default_ordering_fields)


def single_entry_point_of_view(request, *args, **kw):
    lg = logging.getLogger('django-crontab-monitor')
    kw['request'] = request
    kw['executed_from'] = kw.get('executed_from', 'view')
    single_entry_point(*args, **kw)
    message = 'Done from single_entry_point_of_view'
    lg.info(message)
    return HttpResponse(message)