# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Program(models.Model):
    """ Program """
    ######################
    # Private Attributes #
    ######################
    _name = 'school.program'
    _description = "School program"
    _order = 'parent_name, display_name'
    _inherit = ['school.mixin.with.code']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(translate=True)
    parent_name = fields.Char(compute='compute_parent_full_name', store=True)

    school_id = fields.Many2one('school.school', group_expand='_expand_schools', required=True)
    school_district_id = fields.Many2one('school.district', related='school_id.district_id', store=True)

    period_ids = fields.One2many('school.period', 'program_id')

    grade_level_ids = fields.One2many('school.grade.level', 'program_id')
    parent_id = fields.Many2one('school.program')
    child_ids = fields.One2many('school.program', 'parent_id')
    course_ids = fields.Many2many(
        'school.course',
        relation="course_program_relation",
        column1="program_id",
        column2="course_id",)
    
    @api.depends('parent_id', 'parent_id.display_name')
    def compute_parent_full_name(self):
        for program in self:
            if program.parent_id:
                program.parent_name = program.parent_id._get_recursive_parent_name()
            else:
                program.parent_name = program._get_recursive_parent_name()

    def _get_recursive_parent_name(self):
        self.ensure_one()
        name = self._get_name_with_code()
        if self.parent_id:
            name = "%s / %s" % (self.parent_id._get_recursive_parent_name(), name)
        return name

    @api.model
    def display_name_depends(self):
        return ['code',
                'name',
                'parent_id',
                'parent_id.name',
                'parent_id.code',
                'parent_id.display_name']

    @api.depends(lambda self: self.display_name_depends())
    def compute_name(self):
        for record in self:
            record.display_name = record._get_recursive_parent_name()

    ##################
    # Compute method #
    ##################
    def _expand_schools(self, states, domain, order):
        company_ids = self.env.companies
        return company_ids.district_ids.school_ids

    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def create(self, vals):
        res = super().create(vals)
        return res

    def write(self, vals):
        res = super().write(vals)
        return res
