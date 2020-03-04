# -*- coding: utf-8 -*-
import logging, urllib, time
from django.utils.translation import gettext as _
from django.utils.timezone import now
from crontab_monitor.models import SelectOption, single_entry_point


def single_entry_point_of_crontab(*args, **kw):
    lg = logging.getLogger('django-crontab-monitor')
    kw['executed_from'] = kw.get('executed_from', 'crontab')
    single_entry_point(*args, **kw)
    message = 'Done from single_entry_point_of_crontab'
    lg.info(message)


def check_outside_web(alert_log, *args, web_urls='https://www.google.com/|https://www.ho600.com/', **kw):
    lg = logging.getLogger('django-crontab-monitor')
    lg.debug("alert_log id: {}".format(alert_log.id))
    lg.debug("web_urls: {}".format(web_urls))
    web_urls = web_urls.split('|')
    title = _('No alarm, just logging')
    status = SelectOption.objects.get(swarm='alert-log-status', value='LOG')
    mail_body = "Executed from {}\n".format(kw.get('executed_from', '__none__'))
    mail_body += "args: {}\n".format(args)
    mail_body += "kw: {}\n".format(kw)
    t0 = time.time()
    for url in web_urls:
        lg.debug("url: {}".format(url))
        try:
            res = urllib.request.urlopen(url)
        except Exception as e:
            status = SelectOption.objects.get(swarm='alert-log-status', value='ALARM')
            title = _('Alarm on {url}').format(url=url)
            mail_body += 'Exception: {}\n'.format(e)
        else:
            if res.status == 200:
                t1 = time.time()
                mail_body += 'Duration of {}: {} seconds\n'.format(url, t1-t0)
                t0 = t1
            else:
                title = _('Alarm on {url}').format(url=url)
                status = SelectOption.objects.get(swarm='alert-log-status', value='ALARM')
                mail_body += '{} Error: {}\n'.format(res.status, res.read())
        if status.value != 'LOG':
            break
    for receiver in alert_log.inspection.get_receive_notification_users():
        alert_log.receivers.add(receiver)
    alert_log.title = title
    alert_log.mail_body = mail_body
    alert_log.status = status
    alert_log.executed_end_time = now()
    alert_log.save()
    lg.info("title: {}".format(alert_log.title))
    lg.info("status: {}".format(alert_log.status))