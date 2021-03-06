.. django-crontab-monitor documentation master file, created by
   sphinx-quickstart on Wed Mar  4 10:19:48 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-crontab-monitor's documentation!
===============================================================================

Overview
-------------------------------------------------------------------------------

Store crontab-based functions in Django Model so that users can add/disable/delete
crontab-based functions on API service rather than login the server to deal
with system crontab configuration.

The minimal interval of the executing function is one minute as Linux crontab.

Requirements
-------------------------------------------------------------------------------

* Python3-3.5+
* Croniter-0.3+
* Django-2.2+
* django-guardian-2.1+
* Django-filter-2.2+
* djangorestframework-3.10+
* djangorestframework-filters-1.0+

Optional
...............................................................................

* django-crontab-0.7+

Installation
-------------------------------------------------------------------------------

.. code-block:: bash

    pip install `<django-crontab-monitor-path>`

Add `'crontab_monitor'` to your `INSTALLED_APPS` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'guardian',
        'rest_framework',
        'django_filters',
        'rest_framework_filters',
        'crontab_monitor',
    ]

Execute single_entry_point_of_management by crontab of Linux
...............................................................................

.. code-block:: bash

    * * * * *   user /path/virtualenv/bin/python3 /path/your_project/manage.py \
                     single_entry_point_of_management parameter1 parameter2

Execute single_entry_point_of_crontab by django-crontab
...............................................................................

.. code-block:: python

    CRONJOBS = [
        ('* * * * *',
         'crontab_monitor.crontabs.single_entry_point_of_crontab',
         ['arg1'], {'key1': 'value1'}),
    ]

Execute single_entry_point_of_view by some monitor services(ex: nodeping)
...............................................................................

Put a path into urlpatterns in urls.py:

.. code-block:: python

    urlpatterns = [
        ...
        path('what_ever_you_want/', include('crontab_monitor.urls'), name='crontab_monitor'),
    ]

Then add a check with url:
https://your_domain/what_ever_you_want/single_entry_point_of_view/?me=nodeping
into nodeping service.

Crontab-based function example: crontab_monitor.crontabs.check_outside_web
...............................................................................

After ./manage.py migrate crontab_monitor, it will create an Inspection object for you.
And we can remove "#" from this inspection.cron_format to enable it.

.. code-block:: python

    Python 3.7.5 (default, Dec  8 2019, 11:41:26) 
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from crontab_monitor.models import *
    In [2]: insp = Inspection.objects.get(name='check_outside_web',
       ...:                               note='An example for showing a well cron function')
    In [3]: vars(insp)
    {'_state': <django.db.models.base.ModelState at 0x10d8a4490>,
     'id': 1,
     'cron_format': '#* * * * *',
     'name': 'check_outside_web',
     'function_option_id': 5,
     'function_note': 'An example for showing a well cron function',
     'kwargs': 'web_urls=https://www.google.com/|https://www.ho600.com/'}
    In [4]: insp.cron_format = insp.cron_format.replace('#', '')
    In [5]: insp.save()
    
If you want to disable this example crontab-based function, then just put a prefix "#"
in inspection.cron_format.

Indices and tables
===============================================================================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
