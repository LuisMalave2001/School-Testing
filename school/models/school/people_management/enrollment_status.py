# -*- coding: utf-8 -*-

from odoo import models, fields

class EnrollmentStatus(models.Model):
    """ Enrollment for students """
    _name = 'school.enrollment.status'
    _description = "Enrollment Status"
    name = fields.Char(string="Name", required=True, translate=True)
    key = fields.Char(
        string="Key", 
        description="This is used mainly for web services")
    note = fields.Char(string="Description")
    type = fields.Selection([
        ('admission', 'Admission'),
        ('enrolled', 'Enrolled'),
        ('graduate', 'Graduate'),
        ('inactive', 'Inactive'),
        ('pre_enrolled', 'Pre-Enrolled'),
        ('withdrawn', 'Withdrawn'),
        ])


class EnrollmentSubStatus(models.Model):
    """ Substatus for students """
    _name = 'school.enrollment.sub.status'
    _description = "Enrollment sub status"

    status_id = fields.Many2one(
        'school.enrollment.status', String='Status')
    name = fields.Char(string="Name", required=True, translate=True)
    key = fields.Char(string="Key")
