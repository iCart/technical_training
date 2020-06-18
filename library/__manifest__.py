# -*- coding: utf-8 -*-
{
    'name': "Library",

    'summary': """
        Library management
    """,

    'description': """
        Library module for Books and Rentals
    """,

    'author': "SyF",
    'website': "http://www.example.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'module_category_extra',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/books.xml',
        'views/authors.xml',
        'views/rentals.xml',
        'views/partners.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True
}
