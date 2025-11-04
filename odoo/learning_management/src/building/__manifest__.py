# -*- coding: utf-8 -*-
{
    'name': "building",

    'depends': ['user_management', 'education'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/building.xml',
        'views/coworking.xml',
        'views/floor.xml',
        'views/room.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

