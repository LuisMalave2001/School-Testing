# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SchoolBaseIndividual(models.Model):
    """ School Family Individual """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.family.individual'
    _description = "Family individual"
    _inherits = {
        'res.partner': 'partner_id',
        }

    ###################
    # Default methods #
    ###################
    @api.model
    def _default_login(self):
        import time
        return 'individual%i' % int(time.time())

    ######################
    # Fields declaration #
    ######################
    partner_name = fields.Char(
        store=False, compute="_compute_name", inverse='_set_name')

    user_id = fields.Many2one('res.users')
    partner_id = fields.Many2one('res.partner')

    active = fields.Boolean(default=True)

    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()

    family_ids = fields.Many2many(
        'school.family',
        relation='individual_family_rel',
        column1='individual_id',
        column2='family_id')
    family_student_ids = fields.Many2many(
        'school.student', string="Family Students",
        help="This are the students in the family",
        related='family_ids.student_ids')
    student_ids = fields.One2many('school.student', 'individual_id')
    family_individual_ids = fields.Many2many(
        related='family_ids.individual_ids')
    # this fields isn't really used. It just to prevent odoo from send us
    # exceptions...  
    # user_login = fields.Char( required=True, help="Used to log into the system",

    relationship_ids = fields.Many2many(
        'school.family.individual.relationship',
        compute='compute_relationship_ids')

    parent_relationship_ids = fields.One2many(
        'school.family.individual.relationship',
        string="Parents/Guardian", compute="compute_relationship_ids",
        inverse="_set_parent_relationships", readonly=False)

    sibling_relationship_ids = fields.One2many(
        'school.family.individual.relationship',
        string="Siblings", compute="compute_relationship_ids",
        inverse="_set_sibling_relationships", readonly=False, store=False)

    other_relationship_ids = fields.One2many(
        'school.family.individual.relationship', string="Others",
        compute="compute_relationship_ids",
        inverse="_set_other_relationships", readonly=False, store=False)

    custodial_relationship_ids = fields.Many2many(
        'school.family.individual.relationship', string="Custody contacts",
        compute="compute_relationship_ids", store=False)

    # Address
    families_home_address_ids = fields.Many2many(
        'school.home.address',
        compute='compute_families_home_address_ids')
    home_address_id = fields.Many2one(
        'school.home.address', string="Home Address")

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        self.auto_format_name()

    def _set_name(self):
        for individual in self:
            individual.partner_id.name = individual.partner_name

    def compute_relationship_ids(self):
        """ Compute the relationships of the individual depending on the 
            relationship of their families """
        for individual in self:
            individual.relationship_ids = individual.family_ids.mapped(
                'individual_relationship_ids').filtered_domain([
                    ('individual_id', '=', individual.id),
                    ('individual_id.active', '=', True),
                    ('individual_relation_id.active', '=', True),
                    ])

            parent_types = ['parent', 'father', 'mother']
            sibling_types = ['brother', 'sister', 'sibling']

            parent_ids = individual.relationship_ids.filtered_domain([
                ('relationship_type_id.type', 'in', parent_types)
                ])
            sibling_ids = individual.relationship_ids.filtered_domain([
                ('relationship_type_id.type', 'in', sibling_types)
                ])
            other_ids =\
                individual.relationship_ids.filtered_domain([
                    (
                        'relationship_type_id.type',
                        'not in',
                        parent_types + sibling_types)
                    ])

            custody_ids = individual.relationship_ids.filtered('custody')

            individual.parent_relationship_ids = parent_ids
            individual.sibling_relationship_ids = sibling_ids
            individual.other_relationship_ids = other_ids
            individual.custodial_relationship_ids = custody_ids

    def _set_individual_relationship(self, individual_types=[], rel_field_name=False, exclude_types=False):
        """
            We just use this function to not repeat three times the same code 
        """
        for individual in self:
            default_individual_type = \
                self.env['school.family.individual.relationship.type'].search([
                    ('type', 'in', individual_types)
                    ])[:1]

            def filter_individual(relationship):
                in_operator = 'in' if exclude_types else 'not in'
                return relationship.filtered_domain([
                    ('relationship_type_id.type', in_operator, individual_types),
                    ('individual_id', '=', individual.partner_id.id),
                    ('individual_id.active', '=', True),
                    ('individual_relation_id.active', '=', True),
                    ])

            for family_id in individual.family_ids:
                family_relations = \
                    filter_individual(family_id.individual_relationship_ids)
                rel_to_remove =\
                    family_relations - individual[rel_field_name]
                rel_to_add =\
                    individual[rel_field_name].filtered(
                        lambda r:
                            r.family_id == family_id and
                            r not in family_id.individual_relationship_ids)

                for individual in rel_to_add:
                    if not individual.relationship_type_id.type:
                        individual.relationship_type_id = default_individual_type
                    if individual.individual_id != individual:
                        individual.individual_id = individual

                    family_id.sudo().individual_relationship_ids += individual

                    # Add as family individual if it's new
                    if individual.individual_relation_id not in family_id.individual_ids:
                        family_id.individual_ids += individual.individual_relation_id

                rel_to_remove.write({'relationship_type_id': False})

    def _set_parent_relationships(self):
        """ If you remove someone as parents
            Normally you expect that the person still belong to the family
            So, we just change it"""
        for individual in self:
            parent_types = ['parent', 'father', 'mother']
            field_name = "parent_relationship_ids"
            individual._set_individual_relationship(parent_types, field_name)

    def _set_sibling_relationships(self):
        for individual in self:
            sibling_types = ['sibling', 'father', 'mother']
            field_name = "sibling_relationship_ids"
            individual._set_individual_relationship(sibling_types, field_name)

    def _set_other_relationships(self):
        for individual in self:
            other_types = ['sibling', 'father', 'mother', 'parent', 'father', 'mother']
            field_name = "other_relationship_ids"
            individual._set_individual_relationship(other_types, field_name, exclude_types=True)

    def compute_families_home_address_ids(self):
        for individual in self:
            individual.families_home_address_ids = \
                individual.mapped('family_ids.home_address_ids')

    ############################
    # Constrains and onchanges #
    ############################
    @api.onchange('user_login')
    def onchange_user_login(self):
        for individual in self:
            if not individual.login:
                individual.login = self._default_login()

    #########################
    # CRUD method overrides #
    #########################
    def write(self, vals):
        res = super(SchoolBaseIndividual, self).write(vals)
        self._fields_sync(vals)
        return res

    @api.model
    def create(self, vals):
        res = super(SchoolBaseIndividual, self).create(vals)
        self._fields_sync(vals)
        return res
    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################

    # This fields are mainly used for the onchange method below
    home_address_name = fields.Char(related='home_address_id.name')
    home_address_country_id = fields.Many2one(
        related='home_address_id.country_id')
    home_address_state_id = fields.Many2one(
        related='home_address_id.state_id')

    home_address_city = fields.Char(related='home_address_id.city')
    home_address_zip = fields.Char(related='home_address_id.zip')
    home_address_street = fields.Char(related='home_address_id.street')
    home_address_street2 = fields.Char(related='home_address_id.street2')
    home_address_phone = fields.Char(related='home_address_id.phone')

    @api.onchange('home_address_id',
                  'home_address_country_id',
                  'home_address_state_id',
                  'home_address_city',
                  'home_address_street',
                  'home_address_street2',
                  'home_address_phone', )
    def onchange_home_address_id(self):
        res = {}
        if self.home_address_id:
            address_fields = self.partner_id._address_fields()
            if any(self.home_address_id[key] for key in address_fields):
                def convert(value):
                    return value.id if isinstance(value,
                                                  models.BaseModel) else value

                res['value'] = {key: convert(self.home_address_id[key]) for key
                                in address_fields}
        return res

    @api.onchange('home_address_id', 'home_address_phone')
    def _phone_sync_from_home_address(self):
        for partner in self:
            if partner.home_address_id.phone:
                partner.phone = partner.home_address_id.phone

    def _fields_sync(self, values):
        if values.get('home_address_id'):
            self._phone_sync_from_home_address()
            onchange_vals = self.onchange_home_address_id().get('value', {})
            self.partner_id.update_address(onchange_vals)

    def auto_format_name(self):
        """ Use format_name method to create that """
        for individual in self:
            first = individual.first_name
            middle = individual.middle_name
            last = individual.last_name

            if any([first, middle, last]):
                individual.partner_name = individual.format_name(first, middle,
                                                                 last)
                individual.name = individual.format_name(first, middle, last)
            else:
                individual.partner_name = individual.partner_name
                individual.name = individual.name

    @api.model
    def format_name(self, first_name, middle_name, last_name):
        """
        This will format everything depending of school settings
        :return: A String with the formatted version
        """

        name_order_relation = {
            self.env.ref("school.name_sorting_first_name"):
                first_name or "",
            self.env.ref(
                "school.name_sorting_middle_name"): middle_name or "",
            self.env.ref("school.name_sorting_last_name"): last_name or ""
            }

        name_sorting_ids = self.env.ref(
            "school.name_sorting_first_name") + self.env.ref(
            "school.name_sorting_middle_name") + self.env.ref(
            "school.name_sorting_last_name")

        name = ""
        sorted_name_sorting_ids = name_sorting_ids.sorted("sequence")
        for sorted_name_id in sorted_name_sorting_ids:
            name +=\
                (sorted_name_id.prefix or "") \
                + name_order_relation.get(sorted_name_id, "") \
                + (sorted_name_id.sufix or "")

        return name

    def open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'name': self.partner_name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            }
