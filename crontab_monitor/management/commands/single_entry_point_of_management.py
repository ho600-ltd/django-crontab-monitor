# -*- coding: utf-8 -*-
import logging
from random import random
from hashlib import sha1 as sha

from django.db import DatabaseError
from django.core.management.base import BaseCommand, CommandError
from crontab_monitor.models import single_entry_point


class Command(BaseCommand):
    help = ''' '''


    def add_arguments(self, parser):
        parser.add_argument('parameters', nargs='*', type=str)


    def handle(self, *args, **kw):
        lg = logging.getLogger('django-crontab-monitor')
        kw['parameters'] = kw.get('parameters', [])
        kw['executed_from'] = 'management'
        single_entry_point(*args, **kw)
        lg.info('Done from single_entry_point_of_management')
        