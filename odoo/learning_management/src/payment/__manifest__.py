# -*- coding: utf-8 -*-
{
    'name': ' lms Education Payment Management',
    'version': '1.0',
    'summary': 'Manage student payments by group and course',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['user_management', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/edu_payment.xml',
        'views/costs.xml',
        'views/coupon.xml',
        'views/kpi.xml',
        'views/salary.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
