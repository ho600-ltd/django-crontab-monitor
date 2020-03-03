from rest_framework.renderers import BrowsableAPIRenderer



class CMBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = "crontab_monitor/api.html"


