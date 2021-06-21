# -*- encoding: utf-8 -*-

from odoo import fields, models, api, _


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    class_ids = fields.Many2many(
        'school.class', relation='class_event_rel', column1='event_id', column2='class_id')

    class_id = fields.Many2one('school.class', string="Course class")