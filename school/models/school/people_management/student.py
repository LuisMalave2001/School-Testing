# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SchoolBaseStudent(models.Model):
    """ Student model """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.student'
    _description = "Student"
    _inherits = {
        'school.family.individual': 'individual_id',
        }
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    partner_id = fields.Many2one('res.partner', related='individual_id.partner_id')
    # individual_id = fields.Many2one('school.family.individual')

    # Demographics
    individual_id = fields.Many2one('school.family.individual')
    student_status_id = fields.Many2one('school.enrollment.status')
    grade_level_id = fields.Many2one('school.grade.level')
    date_of_birth = fields.Date()
    gender = fields.Many2one('school.gender')

    phone = fields.Char()
    email = fields.Char()
    email2 = fields.Char()

    # Healthcare
    allergies_ids = fields.One2many(
        "school.healthcare.allergy", "partner_id",
        string="Medical Allergies")
    conditions_ids = fields.One2many(
        "school.healthcare.condition", "partner_id",
        string="Medical conditions")
    medications_ids = fields.One2many(
        "school.healthcare.medication", "partner_id",
        string="Medical Medication")

    doctor_name = fields.Char("Doctor name")
    doctor_phone = fields.Char("Doctor phone")
    doctor_address = fields.Char("Doctor Direction")
    hospital = fields.Char("Hospital")
    hospital_address = fields.Char("Hospital Address")
    permission_to_treat = fields.Boolean("Permission To Treat")
    blood_type = fields.Char("Blood Type")

    # Academic
    program_setting_ids = fields.One2many(
        'school.student.program.setting', 'student_id')
    program_ids = fields.Many2many(
        'school.program', store=True, compute='_compute_school_fields')
    school_ids = fields.Many2many(
        'school.school', store=True, compute='_compute_school_fields')
    grade_level_ids = fields.Many2many(
        'school.grade.level', store=True, compute='_compute_school_fields')

    enrollment_history_ids = fields.One2many('school.enrollment.history', 'student_id')

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends(
        'program_setting_ids',
        'program_setting_ids.school_id',
        'program_setting_ids.program_id',
        'program_setting_ids.grade_level_id',
    )
    def _compute_school_fields(self):
        for student in self:
            student.school_ids = student.mapped('program_setting_ids.school_id')
            student.grade_level_ids = student.mapped('program_setting_ids.grade_level_id')
            student.program_ids = student.mapped('program_setting_ids.program_id')

    ############################
    # Constrains and onchange  #
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


class SchoolStudentProgramSetting(models.Model):
    _name = 'school.student.program.setting'

    student_id = fields.Many2one('school.student', required=True)

    school_id = fields.Many2one('school.school', required=True)
    school_program_ids = fields.One2many('school.program', related='school_id.program_ids')
    program_id = fields.Many2one('school.program', required=True)
    program_grade_level_ids = fields.One2many(
        'school.grade.level', related='program_id.grade_level_ids')
    grade_level_id = fields.Many2one('school.grade.level', required=True)

    @api.onchange('school_id', 'program_id')
    def onchange_school_id(self):
        self.ensure_one()
        other_settings = self.student_id.program_setting_ids - self
        other_program_ids = self.school_id.program_ids - other_settings.mapped('program_id')
        other_grade_level_ids = self.program_grade_level_ids - other_settings.mapped('grade_level_id')
        return {
            'domain': {
                'program_id': [('id', 'in', other_program_ids.ids)],
                'grade_level_id': [('id', 'in', other_grade_level_ids.ids)],
            }
        }
