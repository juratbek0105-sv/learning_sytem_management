# -*- coding: utf-8 -*-
{
    'name': " LMS education_payment",

    'depends': ['lms_education', 'lms_payment'],
    'auto_install': ['lms_education', 'lms_payment'],

    'data': [
        'security/ir.model.access.csv',
        'views/payment.xml',
        'views/schedule_student_lesson.xml',
        'views/schedule_table.xml',
        'views/course.xml',

        'data/cron_withdraw.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

