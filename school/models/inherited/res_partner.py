# # -*- encoding: utf-8 -*-
#
# from odoo import fields, models, api, _
# from odoo.exceptions import AccessError, UserError, ValidationError
#
# from ..utils.commons import switch_statement

SELECT_PERSON_TYPES = [
    ("student", "Student"),
    ("parent", "Parent")
    ]

SELECT_COMPANY_TYPES = [
    ("person", "Person"),
    ("company", "Company/Family")
    ]

SELECT_STATUS_TYPES = [
    ("admissions", "Admissions"),
    ("enrolled", "Enrolled"),
    ("graduate", "Graduate"),
    ("inactive", "Inactive"),
    ("pre-enrolled", "Pre-Enrolled"),
    ("withdrawn", "Withdrawn"),
    ]

SELECT_REENROLLMENT_STATUS = [
    ("open", "Open"),
    ("finished", "Finished"),
    ("withdrawn", "Withdrawn"),
    ("rejected", "Rejected"),
    ("blocked", "Blocked"),
]

#
# class ResPartner(models.Model):
#     """ We inherit to enable School features for contacts """
#
#     ######################
#     # Private Attributes #
#     ######################
#     _inherit = "res.partner"
#
#     ###################
#     # Default methods #
#     ###################
#
#     ######################
#     # Fields declaration #
#     ######################
#
#     # - Demographics
#     name = fields.Char(
#         index=True, compute="_compute_name", store=True, readonly=False)
#
#     # Name should be readonly
#     allow_edit_student_name = fields.Boolean(
#         compute="_retrieve_allow_name_edit_from_config")
#     allow_edit_parent_name = fields.Boolean(
#         compute="_retrieve_allow_name_edit_from_config")
#     allow_edit_person_name = fields.Boolean(
#         compute="_retrieve_allow_name_edit_from_config")
#
#     is_name_edit_allowed = fields.Boolean(
#         compute="_compute_allow_name_edition")
#
#     first_name = fields.Char("First Name")
#     middle_name = fields.Char("Middle Name")
#     last_name = fields.Char("Last Name")
#     date_of_birth = fields.Date(string='Date of birth')
#     suffix = fields.Char("Suffix")
#     facts_nickname = fields.Char("Facts Nickname")
#     ethnicity = fields.Char("Ethnicity")
#     facts_citizenship = fields.Char("Facts Citizenship")
#     primary_language = fields.Char("Primary Language")
#     birth_city = fields.Char("Birth City")
#     birth_state = fields.Char("Birth State")
#     birh_place = fields.Char("Birth place")
#     race = fields.Char("Race")
#     gender = fields.Many2one("school.gender", string="Gender")
#
#     ssn = fields.Char()
#
#     id_documentation_file = fields.Binary(attachment=True)
#     id_documentation_file_name = fields.Char()
#
#     passport_id = fields.Char('Passport ID')
#     passport_expiration_date = fields.Date('Passport expiration date')
#
#     passport_id_file = fields.Binary(attachment=True)
#     passport_id_file_name = fields.Char()
#
#     residency_permit_id_file = fields.Binary(attachment=True)
#     residency_permit_id_file_name = fields.Char()
#
#     citizenship = fields.Many2one("res.country", string="Citizenship")
#     identification = fields.Char("ID number")
#     salutation = fields.Char("Salutation")
#
#     marital_status_id = fields.Many2one(
#         'school.marital_status', string='Marital status')
#
#     occupation = fields.Char("Occupation")
#     title = fields.Char("Title")
#
#     # It is known that Odoo has parent_id.
#     # But sometime the school just doesn't really care about it and
#     # parent_id changes the partner behaviour. So this is more a metadata
#     employer = fields.Char("Employer")
#
#     # - Medical
#
#     # - Conctact

#
#     # - Academic
#     # Fields for current student status, grade leve, status, etc...
#     school_ids = fields.Many2many('school.school')
#     school_grade_ids = fields.One2many(
#         'school.partner_school_grade', 'partner_id')
#
#     school_id = fields.Many2one(
#         'school.school', string='Current school code')
#     grade_level_id = fields.Many2one(
#         "school.grade.level", string="Grade Level")
#
#     school_year_id = fields.Many2one(
#         'school.school.year', string="School year",
#         help="The school year where the student is enrolled")
#
#     student_status = fields.Char(
#         "Student status (Deprecated)", help="(This field is deprecated)")
#
#     student_status_id = fields.Many2one(
#         "school.enrollment.status", string="Student status")
#
#     # Fields for next student status, grade leve, status, etc...
#     next_school_id = fields.Many2one(
#         'school.school', string='Next school code')
#     next_grade_level_id = fields.Many2one(
#         "school.grade.level", string="Next grade level")
#     student_next_status_id = fields.Many2one(
#         "school.enrollment.status", string="Student next status")
#
#     home_address_ids = fields.One2many(
#         "school.home.address", 'family_id', string="Home Addresses", )
#     # family_home_address_ids = fields.One2many(
#     #     related='family_ids.home_address_ids',
#     #     string="Family Home Addresses", )
#     home_address_id = fields.Many2one(
#         "school.home.address", string="Home Address")
#
#     homeroom = fields.Char("Homeroom")
#     class_year = fields.Char("Class year")
#     student_sub_status_id = fields.Many2one(
#         'school.enrollment.sub.status', string="Sub status")
#
#     enrolled_date = fields.Date(string="Enrolled date")
#     graduation_date = fields.Date(string="Graduation date")
#
#     withdraw_date = fields.Date(string="Withdraw date")
#     withdraw_reason_id = fields.Many2one('school.withdraw_reason',
#                                          string="Withdraw reason")
#
#     reenrollment_record_ids = fields.One2many(
#         'school.reenrollment.record', 'partner_id')
#
#     reenrollment_status_id = fields.Selection(
#         SELECT_REENROLLMENT_STATUS, string="Reenrollment Status", store=True,
#         compute='_compute_reenrollment_status')
#     reenrollment_school_year_id = fields.Many2one(
#         'school.school.year', string="Reenollment school year", store=True,
#         compute='_compute_reenrollment_status')
#
#     placement_id = fields.Many2one(
#         'school.placement', string="Placement")
#     # - Finance
#     financial_res_ids = fields.Many2many(
#         "res.partner",
#         string="Financial responsability",
#         relation="partner_financial_res",
#         column1="partner_id",
#         column2="partner_financial_id")
#
#     # - Others
#     facts_approved = fields.Boolean()
#     company_type = fields.Selection(
#         SELECT_COMPANY_TYPES, string="Company Type")
#     person_type = fields.Selection(SELECT_PERSON_TYPES, string="Person Type")
#     comment_facts = fields.Text("Facts Comment")
#     facts_id_int = fields.Integer("Facts id (Integer)")
#     facts_id = fields.Char("Facts id")
#
#     # Facts UDID
#     facts_udid_int = fields.Integer(
#         "Facts UDID (Integer)", compute="_converts_facts_udid_id_to_int",
#         store=True, readonly=True)
#     facts_udid = fields.Char("Facts UDID")
#
#     # Enrollment history
#     enrollment_history_ids = fields.One2many(
#         'school.enrollment.history', 'student_id')
#
#     ##############################
#     # Compute and search methods #
#     ##############################
#     @api.depends('school_grade_ids')
#     def compute_grade_levels(self):
#         for partner_id in self:
#             partner_id.grade_level_ids =\
#                 partner_id.mapped('school_grade_ids.grade_level_id')
#
#     @api.depends("allow_edit_student_name", "allow_edit_parent_name",
#                  "allow_edit_person_name", "person_type")
#     def _compute_allow_name_edition(self):
#         for partner_id in self:
#             # Sumulating switch statement
#             partner_id.is_name_edit_allowed = switch_statement(cases={
#                 "default": partner_id.allow_edit_person_name,
#                 "parent": partner_id.allow_edit_parent_name,
#                 "student": partner_id.allow_edit_student_name,
#                 }, value=partner_id.person_type)
#
#     @api.depends("facts_id")
#     def _converts_facts_id_to_int(self):
#         for partner_id in self:
#             partner_id.facts_id_int = int(partner_id.facts_id) if partner_id.facts_id and partner_id.facts_id.isdigit() else 0
#
#     @api.depends("facts_udid")
#     def _converts_facts_udid_id_to_int(self):
#         for partner_id in self:
#             partner_id.facts_udid_int = int(
#                 partner_id.facts_udid) if partner_id.facts_udid and partner_id.facts_udid.isdigit() else 0
#
#     @api.depends("facts_udid")
#     def _converts_facts_udid_id_to_int(self):
#         for partner_id in self:
#             partner_id.facts_udid_int = int(
#                 partner_id.facts_udid) if partner_id.facts_udid and partner_id.facts_udid.isdigit() else 0
#
#     @api.depends("first_name", "middle_name", "last_name")
#     def _compute_name(self):
#         self.auto_format_name()
#
#     @api.depends('reenrollment_record_ids')
#     def _compute_reenrollment_status(self):
#         for partner_id in self:
#             reenrollment_record_id = partner_id.reenrollment_record_ids.sorted('create_date', reverse=True)[:1]
#             partner_id.reenrollment_school_year_id = reenrollment_record_id.school_year_id.id
#             partner_id.reenrollment_status_id = reenrollment_record_id.reenrollment_status
#
#     def compute_self_relationship_ids(self):
#         for partner_id in self:
#             partner_id.self_relationship_ids = \
#                 partner_id.family_ids.mapped('individual_relationship_ids')\
#                     .filtered_domain([
#                         ('individual_id', '=', partner_id.id),
#                         ('individual_id.active', '=', True),
#                         ('individual_relation_id.active', '=', True),
#                         ])
#
#             parent_types = ['parent', 'father', 'mother']
#             sibling_types = ['brother', 'sister', 'sibling']
#
#             parent_ids = partner_id.self_relationship_ids.filtered_domain([
#                 ('relationship_type_id.type', 'in', parent_types)
#                 ])
#             sibling_ids = partner_id.self_relationship_ids.filtered_domain([
#                 ('relationship_type_id.type', 'in', sibling_types)
#                 ])
#             other_ids = partner_id.self_relationship_ids \
#                 .filtered_domain([
#                 ('relationship_type_id.type', 'not in'
#                  , parent_types + sibling_types)
#                 ])
#
#             custody_ids = partner_id.self_relationship_ids.filtered('custody')
#
#             partner_id.parent_relationship_ids = parent_ids
#             partner_id.sibling_relationship_ids = sibling_ids
#             partner_id.other_relationship_ids = other_ids
#             partner_id.custodial_relationship_ids = custody_ids
#
#     ############################
#     # Constrains and onchanges #
#     ############################
#     @api.onchange('school_ids')
#     def onchange_school_ids(self):
#         for partner_id in self:
#             # We remove all
#             school_ids = partner_id.school_ids._origin
#
#             # Add those which aren't in the list
#             schools_to_add = (
#                     school_ids
#                     - partner_id.school_grade_ids.mapped('school_id'))
#
#             # Remove those that aren't in the school codes list
#             schools_to_remove = (
#                     partner_id.school_grade_ids.mapped('school_id')
#                     - school_ids)
#
#             records_to_remove = partner_id.school_grade_ids.filtered(
#                 lambda school_grade:
#                     school_grade.school_id in schools_to_remove)
#
#             # We add news
#             self.env['school.partner_school_grade'].create([{
#                 'school_id': school.id,
#                 'partner_id': partner_id.id,
#                 'grade_level_id': False
#                 } for school in schools_to_add])
#
#             partner_id.school_grade_ids -= records_to_remove
#
#     @api.onchange("person_type")
#     def _onchange_person_type(self):
#         self._compute_allow_name_edition()
#

#
#     @api.constrains("facts_udid")
#     def _check_facts_udid_id(self):
#         for partner_id in self:
#             if partner_id.facts_udid:
#
#                 if not partner_id.facts_udid.isdigit():
#                     raise ValidationError("Facts id needs to be an number")
#
#                 should_be_unique = self.search_count([("facts_id", "=", partner_id.facts_udid)])
#                 if should_be_unique > 1:
#                     raise ValidationError("Another contact has the same facts udid! (%s)" % partner_id.facts_udid)
#
#     # @api.constrains("facts_id")
#     # def _check_facts_id(self):
#     #     for partner_id in self:
#     #         if partner_id.facts_id:
#     #             if not partner_id.facts_id.isdigit():
#     #                 raise ValidationError("Facts id needs to be an number")
#     #
#     #             should_be_unique = self.search_count(
#     #                 [("facts_id", "=", partner_id.facts_id),
#     #                  ('is_family', '=', partner_id.is_family)])
#     #             if should_be_unique > 1:
#     #                 raise ValidationError(
#     #                     "Another contact has the same facts id! (%s)" % partner_id.facts_id)
#
#     @api.onchange("first_name", "middle_name", "last_name")
#     def _onchange_name_fields(self):
#         self.auto_format_name()
#
#     # @api.constrains('individual_relationship_ids')
#     # def _constrains_individual_relationship_ids(self):
#     #     for partner in self:
#     #         rel_ids_pairs = (
#     #             partner.individual_relationship_ids
#     #                 .filtered(lambda r: r.individual_relation_id.active and r.individual_id.active)
#     #                 .mapped(lambda rel: (rel.individual_id.id, rel.individual_relation_id.id))
#     #         )
#     #         for rel_pair in rel_ids_pairs:
#     #             if rel_ids_pairs.count(rel_pair) > 1:
#     #                 raise UserError(_("Duplicated individual relationships is not supported"))
#     #########################
#     # CRUD method overrides #
#     #########################
#     # @api.model
#     # def create(self, values):
#     #     """ Student custom creation for family relations and other stuffs """
#     #
#     #     # Some constant for making more readeable the code
#     #     # ACTION_TYPE = 0
#     #     # TYPE_REPLACE = 6
#     #     TYPE_ADD_EXISTING = 4
#     #     # TYPE_REMOVE_NO_DELETE = 3
#     #
#     #     if "name" not in values:
#     #         first_name = values["first_name"] if "first_name" in values else ""
#     #         middle_name = values[
#     #             "first_name"] if "middle_name" in values else ""
#     #         last_name = values["last_name"] if "last_name" in values else ""
#     #
#     #         values["name"] = self.format_name(first_name, middle_name,
#     #                                           last_name)
#     #     partners = super().create(values)
#     #
#     #     partners.check_school_fields_integrity()
#     #
#     #     ctx = self._context
#     #     for record in partners:
#     #         if "individual_id" in ctx:
#     #             if ctx.get("individual_id"):
#     #                 record.write({
#     #                     "individual_ids": [
#     #                         [TYPE_ADD_EXISTING, ctx.get("individual_id"), False]]
#     #                     })
#     #             else:
#     #                 raise UserError(
#     #                     _("Contact should be save before adding families"))
#     #
#     #     return partners
#     #
#     # def write(self, values):
#     #     """ Student custom creation for family relations and other stuffs """
#     #
#     #     # Some constant for making more readeable the code
#     #     ACTION_TYPE = 0
#     #     TYPE_CREATE = 0
#     #     TYPE_REPLACE = 6
#     #     TYPE_ADD_EXISTING = 4
#     #     TYPE_REMOVE_NO_DELETE = 3
#     #     TYPE_REMOVE_DELETE = 2
#     #
#     #     for partner_id in self:
#     #         if "family_ids" in values:
#     #             for m2m_action in values["family_ids"]:
#     #                 if m2m_action[ACTION_TYPE] == TYPE_REPLACE:
#     #                     family_ids = self.browse(m2m_action[2])
#     #                     removed_family_ids = partner_id.family_ids - family_ids
#     #                     new_family_ids = family_ids - partner_id.family_ids
#     #
#     #                     # Adding myself as a family's individual
#     #
#     #                     for family_id in new_family_ids:
#     #                         new_relationship_values = []
#     #                         for individual in family_id.individual_ids:
#     #                             if not family_id.individual_relationship_ids.filtered(lambda r: r.individual_id == individual and r.individual_relation_id == partner_id):
#     #                                 new_relationship_values.append((TYPE_CREATE, 0, {
#     #                                     'individual_id': individual.id,
#     #                                     'individual_relation_id': partner_id.id,
#     #                                     }))
#     #                             if not family_id.individual_relationship_ids.filtered(lambda r: r.individual_id == partner_id and r.individual_relation_id == individual):
#     #                                 new_relationship_values.append((TYPE_CREATE, 0, {
#     #                                     'individual_id': partner_id.id,
#     #                                     'individual_relation_id': individual.id,
#     #                                     }))
#     #
#     #                         family_id.write({
#     #                             'individual_ids': [[TYPE_ADD_EXISTING, partner_id.id, False]],
#     #                             'individual_relationship_ids': new_relationship_values,
#     #                             })
#     #
#     #                     # Removing myself as a family's individual
#     #                     relations_to_remove = \
#     #                         removed_family_ids.individual_relationship_ids \
#     #                             .filtered_domain([
#     #                             '|',
#     #                             ('individual_id', '=', partner_id.id),
#     #                             ('individual_relation_id', '=', partner_id.id)
#     #                             ])
#     #
#     #                     removed_family_ids.write({
#     #                         'individual_ids': [[TYPE_REMOVE_NO_DELETE, partner_id.id, False]],
#     #                         'individual_relationship_ids': [(TYPE_REMOVE_DELETE, relation.id, 0) for relation in relations_to_remove],
#     #                         })
#     #
#     #         if "individual_ids" in values:
#     #             for m2m_action in values["individual_ids"]:
#     #                 if m2m_action[ACTION_TYPE] == TYPE_REPLACE:
#     #                     individual_ids = self.browse(set(m2m_action[2]))
#     #                     removed_individual_ids = partner_id.individual_ids - individual_ids
#     #
#     #                     # Adding myself as a family of the individual
#     #                     individual_ids.write({
#     #                         "family_ids": [
#     #                             (TYPE_ADD_EXISTING, partner_id.id, False)],
#     #                         })
#     #                     new_individual_ids = individual_ids - partner_id.individual_ids
#     #                     relationship_values = values.get('individual_relationship_ids', [])
#     #                     for new_individual_id in new_individual_ids:
#     #                         for individual in individual_ids.filtered(lambda m: m != new_individual_id):
#     #                             if not partner_id.individual_relationship_ids.filtered(lambda m: m.individual_id == individual and m.individual_relation_id == new_individual_id):
#     #                                 relationship_values.append((TYPE_CREATE, 0, {
#     #                                     'individual_id': individual.id,
#     #                                     'individual_relation_id': new_individual_id.id,
#     #                                     }))
#     #                             if not partner_id.individual_relationship_ids.filtered(lambda m: m.individual_relation_id == individual and m.individual_id == new_individual_id):
#     #                                 relationship_values.append((TYPE_CREATE, 0, {
#     #                                     'individual_id': new_individual_id.id,
#     #                                     'individual_relation_id': individual.id,
#     #                                     }))
#     #
#     #                     # Remove duplicated
#     #                     no_duplicated = set(map(lambda rel: (rel[0], rel[1], tuple(rel[2].items())), relationship_values))
#     #                     relationship_values = list(map(lambda rel: (rel[0], rel[1], dict(rel[2])), no_duplicated))
#     #
#     #                     # Removing myself as a family of the individual
#     #                     relations_to_remove = \
#     #                         partner_id.individual_relationship_ids \
#     #                             .filtered_domain([
#     #                             '|',
#     #                             ('individual_id', 'in', removed_individual_ids.ids),
#     #                             ('individual_relation_id', 'in', removed_individual_ids.ids)
#     #                             ])
#     #                     removed_individual_ids.write({
#     #                         "family_ids": [
#     #                             [TYPE_REMOVE_NO_DELETE, partner_id.id, False]],
#     #                         })
#     #                     relationship_values.extend([
#     #                         (TYPE_REMOVE_DELETE, relation.id, 0)
#     #                         for relation in relations_to_remove])
#     #                     values['individual_relationship_ids'] = relationship_values
#     #
#     #     res = super().write(values)
#     #     # self.generate_missing_relationships
#     #     self.check_school_fields_integrity()
#     #     return res
#
#     ##################
#     # Action methods #
#     ##################
#
#     ####################
#     # Business methods #
#     ####################
#
#     # Overwritten fields
#     # Name should be readonly
#     def _retrieve_allow_name_edit_from_config(self):
#         self.allow_edit_student_name = bool(
#             self.env["ir.config_parameter"].sudo().get_param("school.allow_edit_student_name", False))
#         self.allow_edit_parent_name = bool(
#             self.env["ir.config_parameter"].sudo().get_param("school.allow_edit_parent_name", False))
#         self.allow_edit_person_name = bool(
#             self.env["ir.config_parameter"].sudo().get_param("school.allow_edit_person_name", False))
#

#
#     @api.model
#     def format_name(self, first_name, middle_name, last_name):
#         """
#         This will format everything depending of school settings
#         :return: A String with the formatted version
#         """
#
#         name_order_relation = {
#             self.env.ref(
#                 "school.name_sorting_first_name"): first_name or "",
#             self.env.ref(
#                 "school.name_sorting_middle_name"): middle_name or "",
#             self.env.ref("school.name_sorting_last_name"): last_name or ""
#             }
#
#         name_sorting_ids = self.env.ref(
#             "school.name_sorting_first_name") + \
#                            self.env.ref(
#                                "school.name_sorting_middle_name") + \
#                            self.env.ref("school.name_sorting_last_name")
#
#         name = ""
#         sorted_name_sorting_ids = name_sorting_ids.sorted("sequence")
#         for sorted_name_id in sorted_name_sorting_ids:
#             name += (sorted_name_id.prefix or "") + \
#                     name_order_relation.get(sorted_name_id, "") + \
#                     (sorted_name_id.sufix or "")
#
#         return name
#
#     def auto_format_name(self):
#         """ Use format_name method to create that """
#         # partner_ids = self.filtered(lambda partner: partner_id)
#         for partner_id in self:
#             first = partner_id.first_name
#             middle = partner_id.middle_name
#             last = partner_id.last_name
#
#             if not partner_id.is_company and not partner_id.is_family and any(
#                     [first, middle, last]):
#                 # old_name = partner_id.name
#                 partner_id.name = partner_id.format_name(first, middle, last)
#             else:
#                 partner_id.name = partner_id.name
#
#     # def generate_missing_relationships(self):
#     #     for family_id in self.filtered('is_family'):
#     #         relationship_values = []
#     #         for individual in family_id.individual_ids:
#     #             for aux_individual in family_id.individual_ids.filtered(lambda m: m != individual):
#     #                 if not family_id.individual_relationship_ids.filtered(
#     #                         lambda m: m.individual_id == individual and m.individual_relation_id == aux_individual):
#     #                     relationship_values.append((0, 0, {
#     #                         'individual_id': individual.id,
#     #                         'individual_relation_id': aux_individual.id,
#     #                         }))
#     #                 if not family_id.individual_relationship_ids.filtered(
#     #                         lambda m: m.individual_relation_id == aux_individual and m.individual_id == individual):
#     #                     relationship_values.append((0, 0, {
#     #                         'individual_id': aux_individual.id,
#     #                         'individual_relation_id': individual.id,
#     #                         }))
#     #         if relationship_values:
#     #             no_duplicated = set(map(lambda rel: (rel[0], rel[1], tuple(rel[2].items())), relationship_values))
#     #             relationship_values = list(map(lambda rel: (rel[0], rel[1], dict(rel[2])), no_duplicated))
#     #             family_id.write({'individual_relationship_ids': relationship_values})
#
#     # def check_school_fields_integrity(self):
#     #     for partner in self:
#     #         if (partner.is_family
#     #                 or partner.person_type
#     #                 or partner.individual_ids
#     #                 or partner.family_ids):
#     #             # Email check
#     #             if partner.email:
#     #                 email_partner = self.search([
#     #                     '&',
#     #                     ('email', '=', partner.email),
#     #                     '|', '|', '|',
#     #                     ('is_family', '=', True),
#     #                     ('person_type', '!=', False),
#     #                     ('individual_ids', '!=', False),
#     #                     ('family_ids', '!=', False),
#     #                     ])
#     #                 if email_partner and (len(email_partner) > 1 or email_partner != partner):
#     #                     raise UserError(_(
#     #                         "There is other existing family with the same"
#     #                         " email address, please, use another one"))
#
#     # Helpers methods
#     # devuelve familias de un partner
#     def get_families(self):
#         PartnerEnv = self.env["res.partner"].sudo()
#         return PartnerEnv.search([("is_family", "=", True)]).filtered(
#             lambda app: self.id in app.individual_ids.ids)
#
#     def set_individual_relationship(self, individual_id: int, relation_id: int, reltype_id: int = False):
#         self.ensure_one()
#         if not self.is_family:
#             raise UserError("You only can modify individual relationship from families")
#
#         relationship = \
#             self.individual_relationship_ids.filtered(
#                 lambda rel:
#                     rel.individual_id.id == individual_id
#                     and rel.individual_relation_id.id == relation_id)
#
#         if not relationship:
#             relationship = self.env['school.family.individual.relationship'].create({
#                 'individual_id': individual_id,
#                 'individual_relation_id': relation_id,
#                 'family_id': self.id
#                 })
#         relationship.relationship_type_id = reltype_id
#         return relationship
