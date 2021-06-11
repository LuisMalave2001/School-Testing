# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    district_id = fields.Many2one('school.district', string="District code")
    school_id = fields.Many2one('school.school', string="School")

    district_ids = fields.Many2many('school.district', string="District codes")
    company_district_ids = fields.Many2many('school.district',
        related='company_ids.district_ids')
    school_ids = fields.Many2many('school.school', string="School codes")
    company_school_ids = fields.Many2many('school.school',
        related='company_ids.school_ids')
    district_school_ids = fields.One2many('school.school',
        related='district_ids.school_ids')
