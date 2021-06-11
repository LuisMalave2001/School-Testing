# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = "School class"

    name = fields.Char()
    description = fields.Text()
    course_id = fields.Many2one('school.course', required=True)
    required_skill_ids = fields.One2many('school.course.required.skill', 'res_id', domain="[('res_model', '=', 'school.class')]")

    program_ids = fields.Many2many('school.program', related='course_id.program_ids')
    student_ids = fields.Many2many(
        'school.student', relation='student_class_rel',
        column1='class_id', column2='student_id')

    period_relation_ids = fields.One2many('school.rel.class.period', 'class_id')
    linked_class_ids = fields.One2many(
        'school.class', 'root_linked_class_id', domain="[('id', '!=', id)]")
    root_linked_class_id = fields.Many2one('school.class')
    employee_ids = fields.Many2many(
        'hr.employee', relation='employee_class_rel',
        column1='class_id', column2='employee_id')
    period_ids = fields.Many2many('school.period', store=True, compute='compute_period_ids')

    @api.depends('period_relation_ids')
    def compute_period_ids(self):
        for course_class in self:
            course_class.period_ids = course_class.mapped('period_relation_ids.period_ids')


class CourseClassPeriod(models.Model):
    _name = 'school.rel.class.period'
    _description = "M2M model for periods and classes"

    class_id = fields.Many2one('school.class', required=True)
    class_program_ids = fields.Many2many('school.program', related='class_id.program_ids')
    program_id = fields.Many2one('school.program', required=True)
    period_category_id = fields.Many2one('school.period.category', required=True)
    period_ids = fields.Many2many('school.period', required=True, )
    other_program_ids = fields.Many2many('school.program', compute='compute_other_programs')

    @api.onchange('class_id')
    def compute_other_programs(self):
        for record in self:
            record.other_program_ids = record.mapped('class_id.period_relation_ids.program_id')

    @api.onchange('period_category_id', 'program_id')
    def clear_periods(self):
        self.period_ids = False
