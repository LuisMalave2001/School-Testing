# -*- coding: utf-8 -*-

from odoo import models, fields


class SchoolCourseRequiredSkill(models.Model):
    """ Just using this to prevent using two different models for class and courses """
    _name = 'school.course.required.skill'

    res_model = fields.Char('Resource Model', readonly=True, required=True)
    res_id = fields.Many2oneReference(
        'Resource ID', model_field='res_model', readonly=True, required=True)
    
    skill_id = fields.Many2one('hr.skill', required=True)
    skill_type_id = fields.Many2one('hr.skill.type', required=True)
    skill_level_id = fields.Many2one('hr.skill.level', required=True, string="Minimum skill level")
    level_progress = fields.Integer(related='skill_level_id.level_progress')

class SchoolClass(models.Model):
    _name = 'school.course'

    name = fields.Char()
    program_ids = fields.Many2many(
        'school.program',
        relation="course_program_relation",
        column1="course_id",
        column2="program_id",)
    class_ids = fields.One2many('school.class', 'course_id')
    required_skill_ids = fields.One2many('school.course.required.skill', 'res_id', domain="[('res_model', '=', 'school.course')]")
