# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from odoo.tools import date_utils
import datetime
import logging

_logger = logging.getLogger(__name__)


class GenerateClassEventWizard(models.TransientModel):
    _name = 'generate.class.event.wizard'
    _description = 'Generate Class Event Wizard'

    class_id = fields.Many2one('school.class', required=True)
    date_start = fields.Date(required=True, default=datetime.date.today())
    date_stop = fields.Date(required=True)

    on_conflict = fields.Selection(
        [('overwrite', "Overwrite existing event"),
         ('no_create', "Don't create event"),
         ('keep', "Keep both events"),
         ('warn', 'Warn in the chatter the conflicting events')
         ], default='no_create', required=True)

    def generate_events(self):
        self.ensure_one()
        # Date range list from today until limit
        datetime_start = datetime.datetime.combine(self.date_start, datetime.time.min)
        datetime_stop = datetime.datetime.combine(self.date_stop, datetime.time.max)

        # date_list = [self.date_start + datetime.timedelta(days=x) for x in range(days_to_limit.days)]
        date_list = date_utils.date_range(datetime_start, datetime_stop, datetime.timedelta(days=1))
        for next_event_date in date_list:
            self.class_id.generate_event(next_event_date.date(), self.on_conflict)
