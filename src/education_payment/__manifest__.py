# -*- coding: utf-8 -*-
{
    'name': " LMS education_payment",

    # any module necessary for this one to work correctly
    'depends': ['education', 'payment'],
    'auto_install': ['education', 'payment'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

