# -*- coding: utf-8 -*-
{
    'name': " LMS control",

    'depends': ['user_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/attendance.xml',
        'views/penalty.xml',
        'views/warning.xml',
        'views/work_hours.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

