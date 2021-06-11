# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# X2M methods codes
ACTION_TYPE = 0
TYPE_CREATE = 0
TYPE_REPLACE = 6
TYPE_ADD_EXISTING = 4
TYPE_REMOVE_NO_DELETE = 3
TYPE_REMOVE_DELETE = 2


class SchoolBaseFamily(models.Model):
    """ Family model """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.family'
    _description = "Family"
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    partner_id = fields.Many2one('res.partner')
    active = fields.Boolean(default=True)

    # individuals
    # student_ids = fields.Many2many(
    #     'school.student',
    #     relation='student_family_rel',
    #     column1='family_id',
    #     column2='student_id')

    individual_ids = fields.Many2many(
        'school.family.individual',
        relation='individual_family_rel',
        column1='family_id',
        column2='individual_id')

    student_ids = fields.Many2many('school.student', compute='compute_student_ids')
    no_student_ids = fields.Many2many('school.family.individual', compute='compute_student_ids')

    individual_relationship_ids = fields.Many2many(
        'school.family.individual.relationship', 'family_id',
        domain="[('individual_relation_id.active', '=', True), "
               "('individual_id.active', '=', True)]",
        string="Relationships individuals",
        compute='compute_individual_relationships', store=True)

    home_address_ids = fields.One2many(
        'school.home.address', 'family_id', string="Home addresses")

    ##############################
    # Compute and search methods #
    ##############################

    def compute_student_ids(self):
        for family in self:
            family.student_ids = family.individual_ids.student_ids
            family.no_student_ids = family.individual_ids.filtered(lambda i: not i.student_ids)

    @api.depends('individual_ids')
    def compute_individual_relationships(self):
        for family in self:
            relationship_values = []

            for individual in self.individual_ids:
                for relation in self.individual_ids:
                    if relation != individual:
                        if not family.individual_relationship_ids.filtered(
                            lambda m: m.individual_id == individual 
                            and m.individual_relation_id == relation):
                            relationship_values.append({
                                'individual_id': individual.id,
                                'individual_relation_id': relation.id,
                                'family_id': family.id
                                })
                        if not family.individual_relationship_ids.filtered(
                            lambda m: m.individual_id == relation 
                            and m.individual_relation_id == individual):
                            relationship_values.append({
                                'individual_id': relation.id,
                                'individual_relation_id': individual.id,
                                'family_id': family.id
                                })

            # Remove duplicated
            no_duplicated = set(map(lambda rel: tuple(rel.items()), relationship_values))
            relationship_values = list(map(lambda rel: dict(rel), no_duplicated))

            relations_to_remove = \
                family.individual_relationship_ids.filtered_domain([
                    '|',
                    ('individual_id', 'not in', family.individual_ids.ids),
                    ('individual_relation_id', 'not in', family.individual_ids.ids)])

            relations_to_remove.unlink()
            relationships = \
                self.env['school.family.individual.relationship'].\
                    create(relationship_values)
            family.individual_relationship_ids = \
                    family.individual_relationship_ids \
                    + relationships

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
    def open_family(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.family',
            'name': self.name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            }
