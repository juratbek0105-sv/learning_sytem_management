# -*- coding: utf-8 -*-
{
    'name': "LMS user_management",



    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/student.xml',
        'views/teacher.xml',
        'views/operator.xml',
        'views/hr.xml',
        'views/ceo.xml',
        'views/branch_ceo.xml',
        'views/accountant.xml',
        'views/work_places.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

