# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class SchoolEnrollmentHistory(models.Model):
    _name = 'school.enrollment.history'
    _description = "Enrollment history"
    _order = 'date'

    student_id = fields.Many2one('school.student', required=True)
    school_id = fields.Many2one('school.school', required=True)
    program_id = fields.Many2one('school.program', required=True)

    # This isn't required because maybe want to "log" some withdraw
    grade_level_id = fields.Many2one('school.grade.level')

    enrollment_status_id = fields.Many2one('school.enrollment.status', required=True)
    enrollment_sub_status_id = fields.Many2one('school.enrollment.sub.status', )

    note = fields.Text()
    date = fields.Datetime(default=datetime.datetime.now())
