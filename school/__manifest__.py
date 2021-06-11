# -*- coding: utf-8 -*-
{
    'name': "School base",

    'summary': """ Common models for eduwebgroup school modules as School Year, Grade Level, etc... """,

    'description': """
        Common models for eduwebgroup school modules
    """,

    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list 'category': 'Administration',
    'version': 'alpha1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'portal',
        'contacts',
        'hr_skills',
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/relationships_rules.xml',
        'security/res_partner_rules.xml',
        'security/school_structure_rules.xml',

        # Records
        'data/school_records.xml',

        'data/menudata.xml',
        'data/name_sorting.xml',
        'data/settings_default.xml',
        'data/gender_data.xml',
        'data/actions/res_partner_actions.xml',

        # Views
        'views/assets.xml',
        # 'views/inherited/res_partner.xml',
        'views/res_company.xml',

        'views/student_views.xml',
        'views/family_views.xml',
        'views/individual_views.xml',

        'views/settings/school_settings_views.xml',
        'views/settings/healthcare_settings.xml',
        'views/settings/school_structure_views.xml',

        'views/portal_views.xml',
        'views/config_views.xml',
        # 'views/views.xml'

        # Wizards
        'wizards/enroll_student_form.xml',
        ],

    'qweb': [
        'static/src/xml/views.xml'
        ],
    'application': True,
}
