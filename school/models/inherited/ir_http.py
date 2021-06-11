# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super(IrHttp, self).session_info()
        user = self.env.user

        if user.has_group('base.group_user'):
            districts = self.env.user.district_ids or self.env['school.district'].search([])
            schools = self.env.user.school_ids or self.env['school.school'].search([])
            current_school = schools[:1].read(['name'])[0]
            current_school['district_id'] = schools[0].district_id.id

            school_vals_list = []
            for i, school_vals, in enumerate(schools.read(['name'])):
                school_vals['district_id'] = schools[i].district_id.id
                school_vals_list.append(school_vals)

            session_info.update({
                'user_districts': {
                    'current_district': districts[0].read(['name'])[0],
                    'allowed_districts': districts.read(['name'])
                    },
                'user_schools': {
                    'current_school': current_school,
                    'allowed_schools': school_vals_list,
                    },
                'display_switch_school_menu': bool(self.env.user.district_ids)
                })

        return session_info
