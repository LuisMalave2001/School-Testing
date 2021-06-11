from odoo import _
from odoo.api import Environment
from odoo.exceptions import AccessError
from odoo.tools import lazy_property


def district(self):
    district_ids = self.context.get('allowed_district_ids', [])
    if district_ids:
        if not self.su:
            user_district_ids = self.user.district_ids.ids
            if user_district_ids:
                if any(did not in district_ids for did in district_ids):
                    raise AccessError(_("Access to unauthorized or invalid district codes."))
            return self['school.district'].browse(district_ids[0])
    return self.user.district_id


def districts(self):
    district_ids = self.context.get('allowed_district_ids', [])
    if district_ids:
        if not self.su:
            user_district_ids = self.user.district_ids.ids
            if user_district_ids:
                if any(did not in district_ids for did in district_ids):
                    raise AccessError(_("Access to unauthorized or invalid district codes."))
            return self['school.district'].browse(district_ids)
    return self.user.district_id


def school(self):
    school_ids = self.context.get('allowed_school_ids', [])
    if school_ids:
        if not self.su:
            user_school_ids = self.user.school_ids.ids
            if user_school_ids:
                if any(did not in school_ids for did in school_ids):
                    raise AccessError(_("Access to unauthorized or invalid school codes."))
            return self['school.school'].browse(school_ids[0])
    return self.user.school_id


def schools(self):
    school_ids = self.context.get('allowed_school_ids', [])
    if school_ids:
        if not self.su:
            user_school_ids = self.user.school_ids.ids
            if user_school_ids:
                if any(did not in school_ids for did in school_ids):
                    raise AccessError(_("Access to unauthorized or invalid school codes."))
            return self['school.school'].browse(school_ids)
    return self.user.school_id


Environment.district = lazy_property(district)
Environment.districts = lazy_property(districts)
Environment.school = lazy_property(school)
Environment.schools = lazy_property(schools)
