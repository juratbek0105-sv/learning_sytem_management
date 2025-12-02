# -*- coding: utf-8 -*-
{
    'name': "LMS user_management",



    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/workers.xml',
        'views/work_places.xml',
        'views/partner.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

