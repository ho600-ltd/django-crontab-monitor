import re, logging, datetime, re
from croniter import croniter

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import utc, now
from django.utils.translation import ugettext as _
from guardian.shortcuts import get_users_with_perms

from crontab_monitor import CrontabJob



class SelectOption(models.Model):
    swarm = models.CharField(verbose_name='Swarm Name', max_length=64)
    value = models.CharField(verbose_name='Value', max_length=255)



    class Meta:
        unique_together = (('swarm', 'value', ), )



    def __str__(self):
        return '%s>%s' % (self.swarm, self.value)



class Inspection(models.Model):
    cron_format = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    function_option = models.ForeignKey(SelectOption, on_delete=models.CASCADE)
    function_note = models.TextField()
    kwargs = models.TextField()


    class Meta:
        permissions = (
            ("edit_inspection", "Edit Inspection"),
            ("receive_notification_mail", "Receive Notification Mail"),
            ("view_alert_log", "View Alert Log"),
            ("edit_alert_log", "Edit Alert Log"),
        )


    def __str__(self):
        return '"%s" %s, %s' % (self.cron_format, self.function_option.value, self.name)


    def get_receive_notification_users(self):
        lg = logging.getLogger('django-crontab-monitor')
        users = [u for u in User.objects.filter(is_superuser=True)]
        if (not getattr(settings, 'BASE_URL', "")
            or '127.0.0.1' in settings.BASE_URL.lower()
            or 'localhost' in settings.BASE_URL.lower()):
            lg.debug("settings.BASE_URL: {}".format(getattr(settings, 'BASE_URL', "")))
        else:
            anyperms = get_users_with_perms(self,
                                            attach_perms=True,
                                            with_superusers=False)
            for user, perms in anyperms.items():
                if "receive_notification_mail" in perms:
                    users.append(user)
        lg.debug("get_receive_notification_users: {}".format(users))
        return users


    def save(self, *args, **kwargs):
        """ https://pypi.org/project/croniter/#usage
        """
        if not croniter.is_valid(re.sub('^#', '', self.cron_format)):
            raise Exception('Invalid crontab pattern')
        return super(Inspection, self).save(*args, **kwargs)


class AlertLog(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    executed_end_time = models.DateTimeField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)
    executed_time_ymdhm = models.CharField(max_length=12)
    status = models.ForeignKey(SelectOption, on_delete=models.CASCADE) #LOG/ALARM/CONTACTED/FIXED
    title = models.CharField(max_length=255) #INFO: vangw, return_code, fails count
    receivers = models.ManyToManyField(User)
    mail_body = models.TextField()
    objects_content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id_list = models.TextField()
    @property
    def object_list(self):
        ids = self.object_id_list.split(',')
        model = self.objects_content_type.model_class()
        return model.objects.filter(id__in=ids)



def single_entry_point(*args, **kw):
    NOW = now()
    BASE = NOW - datetime.timedelta(minutes=1)
    LOG = SelectOption.objects.get(swarm='alert-log-status', value='LOG')

    lg = logging.getLogger('django-crontab-monitor')
    lg.debug('NOW: {}; BASE: {}'.format(NOW, BASE))
    for inspection in Inspection.objects.exclude(cron_format__startswith='#'
                                                ).filter(function_option__value__contains='.crontabs.'
                                                        ).order_by('id'):
        if not croniter.is_valid(inspection.cron_format):
            lg.error("Inspection(id: {})'s cron_format Error: {}".format(inspection.id, inspection.cron_format))
            continue

        iter = croniter(inspection.cron_format, BASE)
        EXECUTE_TIME = iter.get_next(datetime.datetime)
        lg.debug('EXECUTE_TIME: {}'.format(EXECUTE_TIME))
        NOW_YmdHM = NOW.strftime('%Y%m%d%H%M')
        EXECUTE_TIME_YmdHM = EXECUTE_TIME.strftime('%Y%m%d%H%M')
        if NOW_YmdHM != EXECUTE_TIME_YmdHM:
            lg.debug("{} != {}".format(NOW_YmdHM, EXECUTE_TIME_YmdHM))
        elif AlertLog.objects.filter(inspection=inspection,
                                     executed_time_ymdhm=EXECUTE_TIME_YmdHM).exists():
            lg.debug('Executed {} with {} at {}'.format(inspection.function_option.value,
                                                        inspection.kwargs,
                                                        EXECUTE_TIME_YmdHM))
        else:
            lg.debug('Executing {} with {}'.format(inspection.function_option.value, inspection.kwargs))
            al = AlertLog(inspection=inspection,
                          status=LOG,
                          executed_time_ymdhm=EXECUTE_TIME_YmdHM,
                          title="executing",
                          mail_body="executing",
                          object_id_list="")
            al.save()
            args = [al] + list(args)

            kwargs = kw
            for kv in inspection.kwargs.split(','):
                if '=' in kv:
                    k, v = kv.split('=')
                    kwargs[k] = v
            
            packages = inspection.function_option.value.split('.')
            function = __import__(".".join(packages[:-1]))
            for p in packages[1:]:
                function = getattr(function, p)
            job = CrontabJob(execute=function,
                             args=args,
                             kwargs=kwargs)
            job.start()
