# -*- coding: utf-8 -*-
{
    'name': "LMS Payment",

    'depends': ['user_management', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/edu_payment.xml',
        'views/costs.xml',
        'views/coupon.xml',
        'views/kpi.xml',
        'views/salary.xml',
        'views/menu.xml',
    ],
}

