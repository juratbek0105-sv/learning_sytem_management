# -*- coding: utf-8 -*-
{
    'name': " LMS education_payment",

    'depends': ['lms_education', 'lms_payment'],
    'auto_install': ['lms_education', 'lms_payment'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/inherit.xml',
        'views/refuel_balance.xml',
        'views/menu.xml',

        'data/cron_withdraw.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

