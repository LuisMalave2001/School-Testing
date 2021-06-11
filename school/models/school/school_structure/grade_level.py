# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SchoolBaseGradeLevel(models.Model):
    """ Grade levels """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.grade.level'
    _order = "sequence"
    _description = "Grade level"
    _inherit = ['school.mixin.with.code', 'image.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    sequence = fields.Integer(default=1)
    program_id = fields.Many2one('school.program')
    school_id = fields.Many2one('school.school', related='program_id.school_id', store=True)
    district_id = fields.Many2one(related="school_id.district_id", store=True)
    capacity = fields.Integer()

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
