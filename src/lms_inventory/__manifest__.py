# -*- coding: utf-8 -*-
{
    'name': " LMS inventory",


    # any module necessary for this one to work correctly
    'depends': ['user_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/device.xml',
        'views/material.xml',
        'views/needs.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

