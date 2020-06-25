# -*- coding: utf-8 -*-
{
    'name':        "OpenAcademy",

    'summary':
                   """
                   Openacademy""",

    'description': """
        Manage course, classes, teachers, students, ...
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'OpenAcademy',
    'version':     '0.3',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'mail'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "security/groups.xml",
        "views/course_views.xml",
        "views/session_views.xml",
        "views/menu_views.xml",
        "data/openacademy_data.xml",
        "data/email_template_data.xml",
        "wizards/add_attendees.xml"
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}
