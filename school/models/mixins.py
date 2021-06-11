# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolBaseMixinWithCode(models.AbstractModel):
    """ It is used mainly in system parameters models to produce a name like
        name - code or just name """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.mixin.with.code'
    _description = "Mixin code"
    _rec_name = 'display_name'

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(required=True, translate=True)
    display_name = fields.Char(compute='compute_name', store=True)
    code = fields.Char()
    active = fields.Boolean(default=True)

    def _get_name_with_code(self):
        self.ensure_one()
        if self.code:
            name = "%s - (%s)" % (self.name, self.code)
        else:
            name = self.name
        return name

    @api.model
    def display_name_depends(self):
        return ['code', 'name']

    @api.depends(lambda self: self.display_name_depends())
    def compute_name(self):
        for record in self:
            record.display_name = record._get_name_with_code()
