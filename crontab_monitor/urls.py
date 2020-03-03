from django.urls import include, re_path, path
from django.conf import settings
from rest_framework import routers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from crontab_monitor.renderers import CMBrowsableAPIRenderer
from crontab_monitor import views as cm_views

urlpatterns = []

class CrontabMonitorAPIRootView(routers.APIRootView):
    """ Endpoints of Crontab Monitor Api
    """
    version = 'v1'
    permission_classes = (IsAdminUser, )
    renderer_classes = (CMBrowsableAPIRenderer, JSONRenderer, )



class CMRouter(routers.DefaultRouter):
    """ The **Class Name**(CrontabMonitorAPIRootView) will be
        the "page-header name" in the "Browseble Api Root Page"
        and
        The __doc__ of CrontabMonitorAPIRootView class will be
        the description in the "Browseble Api Root Page"
    """
    APIRootView = CrontabMonitorAPIRootView



router = CMRouter()
router.register('select_option', cm_views.SelectOptionModelViewSet, basename="select_option")
router.register('inspection', cm_views.InspectionModelViewSet, basename="inspection")
router.register('alert_log', cm_views.AlertLogModelViewSet, basename="alert_log")

urlpatterns += [
    path('api/{}/'.format(CrontabMonitorAPIRootView.version),
         include((router.urls, 'crontab_monitor_api_root'),
                  namespace="crontab_monitor_api_root")),
    path('single_entry_point_of_view/', cm_views.single_entry_point_of_view),
]
