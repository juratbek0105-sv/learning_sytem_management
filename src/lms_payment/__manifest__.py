# -*- coding: utf-8 -*-
{
    'name': ' LMS Payment ',
    'version': '1.0',
    'summary': 'Manage student payments by group and course',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['user_management', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
