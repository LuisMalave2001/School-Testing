# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class EnrollStudentForm(models.TransientModel):
    """ Enrollment Students Form """
    _name = 'enroll.student.form'
    _description = ' Enrollment Students Form '

    name = fields.Char("Name")

    state = fields.Selection([
        ("1", "Students"),
        ("2", "Family"),
        ("3", "Relationship"), ('done', "Done"),
        # ("4", "Finance"),
        ], default="1")

    student_ids = fields.One2many('enroll.student.form.student', 'form_id')

    add_family = fields.Selection([
        ('new', "Add New Family"),
        ('existing', "Add Existing Family"),
    ])

    family_ids = fields.Many2many('school.family')

    family_edit_relationship_id = fields.Many2one('school.family')
    family_relationship_ids = fields.Many2many(
        'enroll.student.form.relationship', ondelete='cascade', store=True,
        compute='compute_family_relationship_ids')

    # noinspection PyProtectedMember
    @api.depends('family_ids')
    def compute_family_relationship_ids(self):
        self.ensure_one()
        relationship_env = self.env['enroll.student.form.relationship']

        # Set relationships
        relationship_vals = []
        for family in self.family_ids:
            for individual in family.individual_ids:
                for student in self.student_ids:
                    relationship_vals.append({
                        'family_id': family.id,
                        'individual_id': student.id,
                        'individual_relation_id': individual.id,
                        })
        relationships = relationship_env.create(relationship_vals)
        self.family_relationship_ids = relationships

    def move_next_step(self):
        self.ensure_one()
        next_state = str(int(self.state) + 1)
        if next_state in dict(self._fields['state'].selection).keys():
            self.state = next_state

    def move_prev_step(self):
        self.ensure_one()
        next_state = str(int(self.state) - 1)
        if next_state in dict(self._fields['state'].selection).keys():
            self.state = next_state

    def enroll(self):
        self.ensure_one()

        # Create associate to family
        # For now, the families are already created...

        # Create individuals
        # Individuals aren't being created yer

        # Create student
        students = self.student_ids.create_students(family_ids=self.family_ids)

        # Create relationships
        self.family_ids.compute_individual_relationships()
        for family in self.family_ids():
            for form_student in self.students:
                student = form_student.create_students(family_ids=family)
                for individual in self.family_ids.no_student_ids:
                    form_relation = self.family_relationship_ids \
                            .filtered(lambda rel: 
                                      rel.individual_id == form_student
                                      and rel.individual_relation_id == individual
                                      and rel.family_id == family)
                    print(form_relation)


class EnrollStudentFormStudent(models.TransientModel):
    _name = 'enroll.student.form.student'
    _rec_name = 'name'

    name = fields.Char(store=True, compute="_compute_name")

    avatar = fields.Binary()

    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()

    student_status_id = fields.Many2one('school.enrollment.status')
    grade_level_id = fields.Many2one('school.grade.level')
    date_of_birth = fields.Date()
    gender = fields.Many2one('school.gender')
    form_id = fields.Many2one('enroll.student.form')

    program_setting_ids = fields.One2many(
        'enroll.student.form.program.setting', 'student_form_id')

    phone = fields.Char()
    email = fields.Char()
    email2 = fields.Char()

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for student in self:
            student.name = self.env['school.family.individual'].format_name(
                student.first_name,
                student.middle_name,
                student.last_name,
                )
            
    def _prepare_student_vals(self):
        self.ensure_one()
        return {
            'name': self.env['school.family.individual'].format_name(self.first_name, self.middle_name, self.last_name),
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'grade_level_id': self.grade_level_id.id,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender.id,
            'phone': self.phone,
            'email': self.email,
            'email2': self.email2,
            'enrollment_history_ids': [(0, 0, {
                'school_id': setting.school_id.id,
                'program_id': setting.program_id.id,
                'grade_level_id': setting.program_id.id,
                'status_id': setting.status_id.id,
                }) for setting in self.program_setting_ids]
            }

    def create_students(self, family_ids=False):
        students = self.env['school.student']
        for form_student in self:
            # I just reuse the create method in students variable
            student = students.create(form_student._prepare_student_vals())
            # Can be false...
            if family_ids:
                for family in family_ids:
                    family.write({
                        'individual_ids': [(4, student.individual_id.id, False)]
                    })


class EnrollStudentFormProgramSettings(models.TransientModel):
    _name = 'enroll.student.form.program.setting'

    student_form_id = fields.Many2one('enroll.student.form.student')

    school_id = fields.Many2one('school.school', required=True)
    program_id = fields.Many2one('school.program', required=True)
    grade_level_id = fields.Many2one('school.grade.level', required=True)
    status_id = fields.Many2one(
        'school.enrollment.status', required=True,
        default=lambda self: self.env['school.enrollment.status'].search([('type', '=', 'enrolled')]))


class EnrollStudentFormRelationship(models.TransientModel):
    _name = 'enroll.student.form.relationship'
    _inherit = 'school.family.individual.relationship' 
    family_id = fields.Many2one(
        "school.family", string="Family", ondelete="cascade", required=False)
    family_individual_ids = fields.Many2many(
        'school.family.individual',
        related='family_id.individual_ids',
        )
    # form_id = fields.Many2one( 'enroll.student.form', required=False)

    # form_student_ids = fields.One2many(
    #     'enroll.student.form.student', related='form_id.student_ids')
    individual_id = fields.Many2one(
        'enroll.student.form.student', string="Individual", required=False, ondelete="cascade")
    individual_relation_id = fields.Many2one(
        "school.family.individual", string="Relation", required=False,
        ondelete="cascade")


# class EnrollStudentFormIndividual(models.TransiejjjjjjntModel):
#     _name = 'enroll.student.form.student.finance'

#     category_id = fields.Many2one('product.category')


class EnrollStudentFormIndividual(models.TransientModel):
    _name = 'enroll.student.form.individual'

    name = fields.Char(store=True, compute="_compute_display_name")

    avatar = fields.Binary()
    
    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()

    student_status_id = fields.Many2one('school.enrollment.status')
    grade_level_id = fields.Many2one('school.grade.level')
    date_of_birth = fields.Date()
    gender = fields.Many2one('school.gender')
    form_id = fields.Many2one('enroll.student.form')

    program_setting_ids = fields.One2many(
          'enroll.student.form.program.setting', 'student_form_id')

    phone = fields.Char()
    email = fields.Char()
    email2 = fields.Char()

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_display_name(self):
        for student in self:
            student.name = self.env['school.family.individual'].format_name(
                student.first_name,
                student.middle_name,
                student.last_name,
                )
